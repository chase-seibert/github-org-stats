Generate per user statistics based on a GitHub organization and a date range.

# Quickstart

To crawl all repos in your organization, and tally number of pull pull requests
and pull request comments by author, since July, 2017.

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python login.py
python comments.py NerdWallet --start 2017-07-01
```
