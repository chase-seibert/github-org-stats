import argparse
from collections import Counter, defaultdict
import time
from login import login_from_credentials


_RESULTS_FILE = 'comments.csv'
stats = defaultdict(lambda: defaultdict(int)) # {'user1': {'author': 1, 'comments': 5}}


def generate_stats(org_name, start_date=None, repo_name=None, pull_id=None, sleep=None):
    gh = login_from_credentials()
    org = gh.organization(org_name)
    for repo in _get_repositories(org, repo_name):
        for pull in _get_pull_requests(repo, pull_id):
            print str(pull.created_at)[:10], pull.html_url
            stats[str(pull.user.login)]['author'] += 1
            if start_date and str(pull.created_at) < start_date:
                break
            # old style comments (no review)
            for comment in pull.issue_comments():
                stats[str(comment.user)]['comments'] += 1
            # new style comments against a review
            for comment in pull.review_comments():
                stats[str(comment.user)]['comments'] += 1
            if sleep:
                time.sleep(sleep)
            write_file()  # in case the process terminates (throttle)
    return stats


def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('org', type=str, help='GitHub organization name')
    parser.add_argument('--start', type=str, help='Start date, format: 2017-01-01')
    parser.add_argument('--repo-name', type=str, help='A single repo name to pull from for testing.')
    parser.add_argument('--pull-request-id', type=int, help='A single pull request ID to pull for testing.')
    parser.add_argument('--sleep', type=int, help='Sleep time in seconds to avoid rate limiting')
    args = parser.parse_args()
    return args


def write_file():
    with open(_RESULTS_FILE, 'w') as fd:
        fd.write('username,pull requests,pull request comments\n')
        for username, counts in stats.items():
            fd.write('%s,%s,%s' % (username, counts['author'], counts['comments']))
            fd.write('\n')


def _get_repositories(org, repo_name=None):
    for repo in org.repositories():
        if repo_name and repo_name != repo.name:
            continue
        yield repo


def _get_pull_requests(repo, pull_id=None):
    for pull in repo.pull_requests(state='all'):
        if pull_id and ('pull/%s' % pull_id) not in pull.html_url:
            continue
        yield pull
        if pull_id:
            break


if __name__ == '__main__':
    # TODO: rate limit? 5000/hr
    options = parse_options()
    stats = generate_stats(
        options.org,
        start_date=options.start,
        repo_name=options.repo_name,
        pull_id=options.pull_request_id,
        sleep=options.sleep,
    )
    print 'Writing to %s' % _RESULTS_FILE
    write_file()
