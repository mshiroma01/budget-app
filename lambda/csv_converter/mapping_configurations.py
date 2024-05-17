# Mapping configurations for different CSV formats
mapping_configs = {
    'chase_credit': {
        'name': 'chase_credit',
        'transaction_date': 'Transaction Date',
        'post_date': 'Post Date',
        'description': 'Description',
        'category': 'Category',
        'transaction_type': 'Type',
        'amount': 'Amount',
        'memo': 'Memo'
    },
    'discover_credit': {
        'name': 'discover_credit',
        'transaction_date': 'Trans. Date',
        'post_date': 'Post Date',
        'description': 'Description',
        'amount': 'Amount',
        'category': 'Category'
    },
    'discover_checking': {
        'name': 'discover_checking',
        'transaction_date': 'Transaction Date',
        'description': 'Transaction Description',
        'transaction_type': 'Transaction Type',
        'debit': 'Debit',
        'credit': 'Credit',
        'balance': 'Balance'
    },
    'bofa_checking': {
        'name': 'bofa_checking',
        'transaction_date': 'Date',
        'description': 'Description',
        'amount': 'Amount',
        'balance': 'Running Bal.'
    },
    'bofa_credit': {
        'name': 'bofa_credit',
        'transaction_date': 'Posted Date',
        'reference_number': 'Reference Number',
        'payee': 'Payee',
        'address': 'Address',
        'amount': 'Amount'
    }
}
