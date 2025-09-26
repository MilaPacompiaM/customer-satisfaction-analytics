#!/usr/bin/env python3
"""
Data Anonymization Functions for Customer Satisfaction Analytics
Implements GDPR-compliant data anonymization techniques
"""

import hashlib
import hmac
import random
import string
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

class DataAnonymizer:
    """GDPR-compliant data anonymization utilities"""

    def __init__(self, salt_key: str = None):
        """Initialize with a secret salt key"""
        self.salt_key = salt_key or self._generate_salt()

    def _generate_salt(self) -> str:
        """Generate a random salt for hashing"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def hash_with_salt(self, value: str) -> str:
        """Apply SHA-256 hashing with salt (irreversible)"""
        if pd.isna(value) or value == '':
            return ''

        combined = f"{value}{self.salt_key}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def pseudonymize_id(self, customer_id: str) -> str:
        """Replace customer ID with pseudonym"""
        if pd.isna(customer_id) or customer_id == '':
            return ''

        # Use HMAC for consistent pseudonymization
        pseudonym = hmac.new(
            self.salt_key.encode(),
            customer_id.encode(),
            hashlib.sha256
        ).hexdigest()[:12]

        return f"CUST_{pseudonym.upper()}"

    def mask_email(self, email: str) -> str:
        """Mask email addresses (partial obfuscation)"""
        if pd.isna(email) or email == '' or '@' not in email:
            return ''

        local, domain = email.split('@')
        if len(local) <= 2:
            masked_local = local[0] + '*' * (len(local) - 1)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]

        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1) + '.' + domain_parts[-1]
        else:
            masked_domain = domain

        return f"{masked_local}@{masked_domain}"

    def mask_phone(self, phone: str) -> str:
        """Mask phone numbers (keep last 4 digits)"""
        if pd.isna(phone) or phone == '':
            return ''

        # Remove non-digit characters
        digits = ''.join(filter(str.isdigit, str(phone)))

        if len(digits) < 4:
            return '*' * len(digits)

        return '*' * (len(digits) - 4) + digits[-4:]

    def anonymize_text(self, text: str, keep_sentiment: bool = True) -> str:
        """Anonymize free text while preserving sentiment"""
        if pd.isna(text) or text == '':
            return ''

        # Replace potential PII patterns
        import re

        # Replace emails
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)

        # Replace phone numbers
        text = re.sub(r'\b\d{3}-?\d{3}-?\d{4}\b', '[PHONE]', text)
        text = re.sub(r'\b\d{10,}\b', '[PHONE]', text)

        # Replace potential names (simple heuristic)
        words = text.split()
        if keep_sentiment:
            # Keep sentiment words, replace potential names
            sentiment_words = ['bueno', 'malo', 'excelente', 'terrible', 'satisfecho', 'insatisfecho']
            for i, word in enumerate(words):
                if len(word) > 3 and word.lower() not in sentiment_words and word[0].isupper():
                    words[i] = '[NOMBRE]'

        return ' '.join(words)

    def aggregate_sensitive_data(self, df: pd.DataFrame,
                                group_cols: List[str],
                                agg_cols: Dict[str, str],
                                min_group_size: int = 3) -> pd.DataFrame:
        """Aggregate data to prevent individual identification"""

        # Group data
        grouped = df.groupby(group_cols).agg(agg_cols).reset_index()

        # Filter groups with minimum size
        group_counts = df.groupby(group_cols).size()
        valid_groups = group_counts[group_counts >= min_group_size].index

        return grouped[grouped.set_index(group_cols).index.isin(valid_groups)]

    def anonymize_customer_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply comprehensive anonymization to customer dataset"""
        df_anon = df.copy()

        # Anonymize identifiers
        if 'customer_id' in df_anon.columns:
            df_anon['customer_id'] = df_anon['customer_id'].apply(self.pseudonymize_id)

        if 'email' in df_anon.columns:
            df_anon['email'] = df_anon['email'].apply(self.mask_email)

        if 'phone' in df_anon.columns:
            df_anon['phone'] = df_anon['phone'].apply(self.mask_phone)

        # Anonymize text fields
        text_columns = ['feedback_text', 'comments', 'description']
        for col in text_columns:
            if col in df_anon.columns:
                df_anon[col] = df_anon[col].apply(self.anonymize_text)

        # Add anonymization metadata
        df_anon['_anonymized_at'] = pd.Timestamp.now()
        df_anon['_anonymization_version'] = '1.0'

        return df_anon

def main():
    """Example usage of anonymization functions"""
    # Example data
    sample_data = pd.DataFrame({
        'customer_id': ['CUST001', 'CUST002', 'CUST003'],
        'email': ['juan.perez@email.com', 'maria.garcia@banco.pe', 'carlos.lopez@gmail.com'],
        'phone': ['987654321', '01-2345678', '999-888-7777'],
        'feedback_text': [
            'Juan Pérez está muy insatisfecho con el servicio',
            'El señor García recomienda el banco a sus amigos',
            'María López tuvo una excelente experiencia'
        ]
    })

    # Initialize anonymizer
    anonymizer = DataAnonymizer()

    # Apply anonymization
    anonymized_data = anonymizer.anonymize_customer_data(sample_data)

    print("Original Data:")
    print(sample_data)
    print("\nAnonymized Data:")
    print(anonymized_data)

if __name__ == "__main__":
    main()