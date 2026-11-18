"""Offline contract tests; fake API responses do not measure LLM quality."""

import copy
import json
import unittest
from types import SimpleNamespace

from pydantic import ValidationError



from reviewsense_genai import (
    EvidenceValidationError, InsightReport, classify_reviews, finding_rows,
    generate_insights, normalize_text, prepare_reviews, validate_report,
)

class EvidenceContractTests(unittest.TestCase):
    def setUp(self):
        self.reviews = [
            {'review_id': 'R01', 'text': 'A comida chegou fria e a bebida não veio.'},
            {'review_id': 'R02', 'text': 'A comida estava deliciosa e veio bem embalada.'},
        ]
        self.payload = {
            'praises': [{'title': 'Sabor', 'description': 'Há um elogio ao sabor.',
                         'evidence': [{'review_id': 'R02', 'quote': 'A comida estava deliciosa'}]}],
            'complaints': [{'title': 'Temperatura', 'description': 'Há uma queixa de comida fria.',
                            'evidence': [{'review_id': 'R01', 'quote': 'A comida chegou fria'}]}],
            'action_suggestions': [{'action': 'Revisar a conservação de temperatura durante a entrega.',
                                    'based_on_review_ids': ['R01']}],
        }

    def test_stringified_finding_is_rejected(self):
        self.payload['complaints'][0] = json.dumps(self.payload['complaints'][0])
        with self.assertRaises(ValidationError):
            generate_insights(self.reviews, client=self.fake_client())

    def test_valid_report_and_computed_counts(self):
        report = validate_report(self.payload, self.reviews)
        self.assertEqual([row['cited_review_count'] for row in finding_rows(report)], [1, 1])

    def test_unknown_id_is_rejected(self):
        self.payload['complaints'][0]['evidence'][0]['review_id'] = 'R99'
        with self.assertRaises(EvidenceValidationError):
            validate_report(self.payload, self.reviews)

    def test_fabricated_quote_is_rejected(self):
        self.payload['complaints'][0]['evidence'][0]['quote'] = 'O entregador ficou perdido.'
        with self.assertRaises(EvidenceValidationError):
            validate_report(self.payload, self.reviews)

    def test_duplicate_evidence_does_not_inflate_counts(self):
        self.payload['complaints'][0]['evidence'] *= 2
        with self.assertRaises(EvidenceValidationError):
            validate_report(self.payload, self.reviews)

    def test_action_cannot_cite_only_a_praise(self):
        self.payload['action_suggestions'][0]['based_on_review_ids'] = ['R02']
        with self.assertRaises(EvidenceValidationError):
            validate_report(self.payload, self.reviews)

    def test_hallucinated_count_field_is_rejected(self):
        self.payload['complaints'][0]['review_count'] = 100
        with self.assertRaises(ValidationError):
            validate_report(self.payload, self.reviews)

    def test_empty_batch_is_rejected(self):
        with self.assertRaises(ValueError):
            prepare_reviews([])

    def test_duplicate_input_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            prepare_reviews([self.reviews[0], self.reviews[0]])

    def test_whitespace_text_is_rejected(self):
        with self.assertRaises(ValueError):
            prepare_reviews([{'review_id': 'R01', 'text': '   '}])

    def test_oversized_batch_is_rejected(self):
        with self.assertRaises(ValueError):
            prepare_reviews([{'review_id': f'R{i}', 'text': 'a' * 2000} for i in range(13)])

    def test_sentiment_preprocessing_preserves_negation_and_accents(self):
        self.assertEqual(normalize_text('  NÃO\tRecomendo！\n'), 'não recomendo!')
        classifier = SimpleNamespace(predict=lambda texts: ['negativo', 'positivo'])
        rows, counts = classify_reviews(self.reviews, classifier)
        self.assertEqual(len(rows), 2)
        self.assertEqual(counts, {'negativo': 1, 'neutro': 0, 'positivo': 1})

    def test_invalid_classifier_result_is_rejected(self):
        with self.assertRaises(ValueError):
            classify_reviews(self.reviews, SimpleNamespace(predict=lambda texts: ['positivo']))

    def fake_client(self, *, status='completed', parsed=True):
        response = SimpleNamespace(
            choices=[SimpleNamespace(
                finish_reason='stop' if status == 'completed' else 'length',
                message=SimpleNamespace(content=json.dumps(self.payload) if parsed else None, refusal=None),
            )],
            model='test-double', id='offline-test-response',
            usage=SimpleNamespace(prompt_tokens=100, completion_tokens=50),
        )
        return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: response)))

    def test_completed_fake_response_passes_contract(self):
        report, metadata = generate_insights(self.reviews, client=self.fake_client())
        self.assertEqual(len(report.complaints), 1)
        self.assertTrue(metadata['reference_integrity_passed'])
        self.assertFalse(metadata['semantic_review_completed'])

    def test_incomplete_response_is_rejected(self):
        with self.assertRaises(RuntimeError):
            generate_insights(self.reviews, client=self.fake_client(status='incomplete'))

    def test_refusal_is_rejected(self):
        with self.assertRaises(RuntimeError):
            generate_insights(self.reviews, client=self.fake_client(parsed=False))

    def test_exact_quote_does_not_prove_semantic_grounding(self):
        payload = copy.deepcopy(self.payload)
        payload['complaints'][0]['description'] = 'O problema foi causado por uma falha no motor da moto.'
        self.assertIsInstance(validate_report(payload, self.reviews), InsightReport)
        # This intentional boundary requires a separate semantic quality evaluation.


