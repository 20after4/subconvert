#!/usr/bin/env python

import os
import sys

from os.path import *

def checkout_and_compare(svn_url, svn_rev, git_dir, git_sha, tmp_dir):
    print 
    if not isdir(tmp_dir):
        os.makedirs(tmp_dir)

    svn_tmp = join(tmp_dir, 'svn')
    git_tmp = join(tmp_dir, 'git')

    if isdir(svn_tmp): os.delete(svn_tmp)
    if isdir(git_tmp): os.delete(git_tmp)

    os.system("svn checkout -r %s file://%s %s" % (svn_rev, svn_url, svn_tmp))

    os.system("git clone %s %s" % (git_dir, git_tmp))
    os.system("git --git-dir=%s checkout %s" % (git_tmp, git_sha))

    try:
        print 'Comparing %s with %s...' % (svn_tmp, git_tmp)

        if os.system("diff -r -U3 -x .svn -x .git %s %s" %
                     (svn_tmp, git_tmp)) != 0:
            print 'Comparison failed for args:', \
                (svn_url, svn_rev, git_dir, git_sha, tmp_dir)
            return False
        else:
            print 'Comparison of SVN rev %s with Git sha %s successful' % \
                (svn_rev, git_sha)
            return True
    finally:
        os.delete(svn_tmp)
        os.delete(git_tmp)

if __name__ == "__main__":
    # What needs to happen here is:
    #
    # 1. Create a list of Git commits in the flat history.
    # 2. Choosing a series of them, read the commit message to find the
    #    corresponding Subversion revision.
    # 3. Call checkout_and_compare to checkout both working trees in both
    #    systems, and then compare them byte-wise for identity.
    # 4. This same algorithm should work for comparing branches with branch
    #    contents in Subversion, but I haven't represented that logic above
    #    yet.
    # 5. This can all likely be done in a much cleaner, more Python-friendly
    #    way, but I was seeking the quickest path to a trustable answer.
    checkout_and_compare(*sys.argv[1:])
