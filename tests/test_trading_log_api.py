import pytest

from application.api.trading_logs import TradingLog


@pytest.fixture()
def trading_log_email_1(session):
    return TradingLog(email='johnwilliam@mail.com')


@pytest.fixture()
def trading_log_email_2(session):
    return TradingLog(email='williamjohn@mail.com')


@pytest.yield_fixture()
def trading_log_with_multiple_emails(session, trading_log_email_1, trading_log_email_2):
    trading_log = Contact(
        username='john',
        first_name='John',
        last_name='William',
    )

    trading_log_emails = [trading_log_email_1, trading_log_email_2]

    trading_log.emails.extend(trading_log_emails)
    session.add(trading_log)
    session.add_all(trading_log_emails)
    yield trading_log

    # Cleanup
    Contact.query.filter(Contact.username == trading_log.username).delete()


@pytest.yield_fixture()
def trading_log_item(session):
    trading_log = Contact(
        username='sam',
        first_name='Sam',
        last_name='Henry',
    )

    trading_log_emails = [
        TradingLog(email='samhenry@mail.com')
    ]

    trading_log.emails.extend(trading_log_emails)
    session.add(trading_log)
    session.add_all(trading_log_emails)
    yield trading_log

    # Cleanup
    Contact.query.filter(Contact.username == trading_log.username).delete()


@pytest.fixture()
def guido_trading_log_data():
    return {
        'username': 'guido',
        'first_name': 'Guido',
        'last_name': 'van Rossum',
        'emails': [
            {
                'email': 'guido@mail.com'
            }
        ]
    }

@pytest.fixture()
def knuth_trading_log_data():
    return {
        'username': 'donald',
        'first_name': 'Donald',
        'last_name': 'Knuth',
        'emails': [
            {
                'email': 'knuth@mail.com',
            },
            {
                'email': 'donald@mail.com'
            }
        ]
    }

@pytest.fixture()
def linus_trading_log_data():
    return {
        'username': 'linus',
        'first_name': 'Linus',
        'last_name': 'Torvalds',
        'emails': [
            {
                'email': 'linus@mail.com',
            }
        ]
    }