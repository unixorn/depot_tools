import unittest
import subprocess2 as subprocess
    self.mox.StubOutWithMock(presubmit.scm.GIT, 'GenerateDiff')
      'GetTrySlavesExecuter', 'GitAffectedFile', 'CallCommand', 'CommandData',
      'SvnAffectedFile', 'SvnChange', 'cPickle', 'cpplint', 'cStringIO',
      'contextlib', 'canned_check_filter', 'fix_encoding', 'fnmatch',
      'gclient_utils', 'glob', 'inspect', 'json', 'load_files', 'logging',
      'marshal', 'normpath', 'optparse', 'os', 'owners', 'pickle',
      'subprocess', 'sys', 'tempfile', 'time', 'traceback', 'types', 'unittest',
      'urllib2', 'warn', 'collections', 'multiprocessing',
  def testGitChange(self):
    description_lines = ('Hello there',
                         'this is a change',
                         'BUG=123',
                         ' STORY =http://foo/  \t',
                         'and some more regular text  \t')
    unified_diff = [
        'diff --git binary_a.png binary_a.png',
        'new file mode 100644',
        'index 0000000..6fbdd6d',
        'Binary files /dev/null and binary_a.png differ',
        'diff --git binary_d.png binary_d.png',
        'deleted file mode 100644',
        'index 6fbdd6d..0000000',
        'Binary files binary_d.png and /dev/null differ',
        'diff --git binary_md.png binary_md.png',
        'index 6fbdd6..be3d5d8 100644',
        'GIT binary patch',
        'delta 109',
        'zcmeyihjs5>)(Opwi4&WXB~yyi6N|G`(i5|?i<2_a@)OH5N{Um`D-<SM@g!_^W9;SR',
        'zO9b*W5{pxTM0slZ=F42indK9U^MTyVQlJ2s%1BMmEKMv1Q^gtS&9nHn&*Ede;|~CU',
        'CMJxLN',
        '',
        'delta 34',
        'scmV+-0Nww+y#@BX1(1W0gkzIp3}CZh0gVZ>`wGVcgW(Rh;SK@ZPa9GXlK=n!',
        '',
        'diff --git binary_m.png binary_m.png',
        'index 6fbdd6d..be3d5d8 100644',
        'Binary files binary_m.png and binary_m.png differ',
        'diff --git boo/blat.cc boo/blat.cc',
        'new file mode 100644',
        'index 0000000..37d18ad',
        '--- boo/blat.cc',
        '+++ boo/blat.cc',
        '@@ -0,0 +1,5 @@',
        '+This is some text',
        '+which lacks a copyright warning',
        '+but it is nonetheless interesting',
        '+and worthy of your attention.',
        '+Its freshness factor is through the roof.',
        'diff --git floo/delburt.cc floo/delburt.cc',
        'deleted file mode 100644',
        'index e06377a..0000000',
        '--- floo/delburt.cc',
        '+++ /dev/null',
        '@@ -1,14 +0,0 @@',
        '-This text used to be here',
        '-but someone, probably you,',
        '-having consumed the text',
        '-  (absorbed its meaning)',
        '-decided that it should be made to not exist',
        '-that others would not read it.',
        '-  (What happened here?',
        '-was the author incompetent?',
        '-or is the world today so different from the world',
        '-   the author foresaw',
        '-and past imaginination',
        '-   amounts to rubble, insignificant,',
        '-something to be tripped over',
        '-and frustrated by)',
        'diff --git foo/TestExpectations foo/TestExpectations',
        'index c6e12ab..d1c5f23 100644',
        '--- foo/TestExpectations',
        '+++ foo/TestExpectations',
        '@@ -1,12 +1,24 @@',
        '-Stranger, behold:',
        '+Strange to behold:',
        '   This is a text',
        ' Its contents existed before.',
        '',
        '-It is written:',
        '+Weasel words suggest:',
        '   its contents shall exist after',
        '   and its contents',
        ' with the progress of time',
        ' will evolve,',
        '-   snaillike,',
        '+   erratically,',
        ' into still different texts',
        '-from this.',
        '\ No newline at end of file',
        '+from this.',
        '+',
        '+For the most part,',
        '+I really think unified diffs',
        '+are elegant: the way you can type',
        '+diff --git inside/a/text inside/a/text',
        '+or something silly like',
        '+@@ -278,6 +278,10 @@',
        '+and have this not be interpreted',
        '+as the start of a new file',
        '+or anything messed up like that,',
        '+because you parsed the header',
        '+correctly.',
        '\ No newline at end of file',
            '']
    files = [('A      ', 'binary_a.png'),
             ('D      ', 'binary_d.png'),
             ('M      ', 'binary_m.png'),
             ('M      ', 'binary_md.png'),  # Binary w/ diff
             ('A      ', 'boo/blat.cc'),
             ('D      ', 'floo/delburt.cc'),
             ('M      ', 'foo/TestExpectations')]

    for op, path in files:
      full_path = presubmit.os.path.join(self.fake_root_dir, *path.split('/'))
      if op.startswith('D'):
        os.path.exists(full_path).AndReturn(False)
      else:
        os.path.exists(full_path).AndReturn(False)
        os.path.isfile(full_path).AndReturn(True)

    presubmit.scm.GIT.GenerateDiff(self.fake_root_dir, files=[], full_move=True
        ).AndReturn('\n'.join(unified_diff))

    self.mox.ReplayAll()

    change = presubmit.GitChange(
        'mychange',
        '\n'.join(description_lines),
        self.fake_root_dir,
        files,
        0,
        0,
        None)
    self.failUnless(change.Name() == 'mychange')
    self.failUnless(change.DescriptionText() ==
                    'Hello there\nthis is a change\nand some more regular text')
    self.failUnless(change.FullDescriptionText() ==
                    '\n'.join(description_lines))

    self.failUnless(change.BUG == '123')
    self.failUnless(change.STORY == 'http://foo/')
    self.failUnless(change.BLEH == None)

    self.failUnless(len(change.AffectedFiles()) == 7)
    self.failUnless(len(change.AffectedFiles(include_dirs=True)) == 7)
    self.failUnless(len(change.AffectedFiles(include_deletes=False)) == 5)
    self.failUnless(len(change.AffectedFiles(include_dirs=True,
                                             include_deletes=False)) == 5)

    # Note that on git, there's no distinction between binary files and text
    # files; everything that's not a delete is a text file.
    affected_text_files = change.AffectedTextFiles()
    self.failUnless(len(affected_text_files) == 5)

    local_paths = change.LocalPaths()
    expected_paths = [os.path.normpath(f) for op, f in files]
    self.assertEqual(local_paths, expected_paths)

    try:
      _ = change.ServerPaths()
      self.fail("ServerPaths implemented.")
    except NotImplementedError:
      pass

    actual_rhs_lines = []
    for f, linenum, line in change.RightHandSideLines():
      actual_rhs_lines.append((f.LocalPath(), linenum, line))

    f_blat = os.path.normpath('boo/blat.cc')
    f_test_expectations = os.path.normpath('foo/TestExpectations')
    expected_rhs_lines = [
        (f_blat, 1, 'This is some text'),
        (f_blat, 2, 'which lacks a copyright warning'),
        (f_blat, 3, 'but it is nonetheless interesting'),
        (f_blat, 4, 'and worthy of your attention.'),
        (f_blat, 5, 'Its freshness factor is through the roof.'),
        (f_test_expectations, 1, 'Strange to behold:'),
        (f_test_expectations, 5, 'Weasel words suggest:'),
        (f_test_expectations, 10, '   erratically,'),
        (f_test_expectations, 13, 'from this.'),
        (f_test_expectations, 14, ''),
        (f_test_expectations, 15, 'For the most part,'),
        (f_test_expectations, 16, 'I really think unified diffs'),
        (f_test_expectations, 17, 'are elegant: the way you can type'),
        (f_test_expectations, 18, 'diff --git inside/a/text inside/a/text'),
        (f_test_expectations, 19, 'or something silly like'),
        (f_test_expectations, 20, '@@ -278,6 +278,10 @@'),
        (f_test_expectations, 21, 'and have this not be interpreted'),
        (f_test_expectations, 22, 'as the start of a new file'),
        (f_test_expectations, 23, 'or anything messed up like that,'),
        (f_test_expectations, 24, 'because you parsed the header'),
        (f_test_expectations, 25, 'correctly.')]

    self.assertEquals(expected_rhs_lines, actual_rhs_lines)

      'LocalToDepotPath', 'Command', 'RunTests',
      'basename', 'cPickle', 'cpplint', 'cStringIO', 'canned_checks', 'change',
      'environ', 'glob', 'host_url', 'is_committing', 'json', 'logging',
      'marshal', 'os_listdir', 'os_walk', 'os_path', 'owners_db', 'pickle',
      'platform', 'python_executable', 're', 'rietveld', 'subprocess', 'tbr',
      'tempfile', 'time', 'traceback', 'unittest', 'urllib2', 'version',
      'verbose',
      ['D', join('foo', 'mat', 'beingdeleted.txt')],
      ['M', join('flop', 'notfound.txt')],
      ['A', join('boo', 'flap.h')],
    fileobj = presubmit.AffectedFile('boo', 'M', 'Unrelated',
                                     diff_cache=mox.IsA(presubmit._DiffCache))
    fileobj = presubmit.AffectedFile('AA/boo', 'M', self.fake_root_dir,
                                     diff_cache=mox.IsA(presubmit._DiffCache))
class OutputApiUnittest(PresubmitTestsBase):

      'PresubmitNotifyResult', 'PresubmitPromptWarning',
      'PresubmitPromptOrNotify', 'PresubmitResult', 'is_committing',
    self.compareMembers(presubmit.OutputApi(False), members)
    output = presubmit.PresubmitOutput(input_stream=StringIO.StringIO('\n'))
    self.failIf(output.should_continue())
    self.failUnless(output.getvalue().count('???'))

    output_api = presubmit.OutputApi(True)
    output = presubmit.PresubmitOutput(input_stream=StringIO.StringIO('y'))
    output_api.PresubmitPromptOrNotify('???').handle(output)
    output.prompt_yes_no('prompt: ')
    self.failUnless(output.should_continue())
    self.failUnless(output.getvalue().count('???'))

    output_api = presubmit.OutputApi(False)
    output = presubmit.PresubmitOutput(input_stream=StringIO.StringIO('y'))
    output_api.PresubmitPromptOrNotify('???').handle(output)
    output_api = presubmit.OutputApi(True)
    output_api.PresubmitPromptOrNotify('???').handle(output)
      'AbsoluteLocalPath', 'Action', 'ChangedContents', 'DIFF_CACHE',
      'GenerateScmDiff', 'IsDirectory', 'IsTextFile', 'LocalPath',
      'NewContents', 'Property', 'ServerPath',
    self.compareMembers(
        presubmit.GitAffectedFile('a', 'b', self.fake_root_dir), members)
def CommHelper(input_api, cmd, ret=None, **kwargs):
  ret = ret or (('', None), 0)
  input_api.subprocess.communicate(
      cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs
      ).AndReturn(ret)


    input_api.subprocess = self.mox.CreateMock(subprocess)
    presubmit.subprocess = input_api.subprocess
    input_api.Command = presubmit.CommandData
    input_api.RunTests = presubmit.InputApi.RunTests
      'GetPythonUnitTests', 'GetPylint',
      'GetUnitTests', 'GetUnitTestsInDirectory',
    check = lambda x, y, _: presubmit_canned_checks.CheckLongLines(x, y, 80)
    check = lambda x, y, _: presubmit_canned_checks.CheckLongLines(x, y, 80)
    check = lambda x, y, _: presubmit_canned_checks.CheckLongLines(x, y, 80)
    output_api = presubmit.OutputApi(False)
    CommHelper(input_api, ['pyyyyython', '-m', '_non_existent_module'],
                    ret=(('foo', None), 1), cwd=None, env=None)
    CommHelper(input_api, ['pyyyyython', '-m', '_non_existent_module'],
                    ret=(('foo', None), 1), cwd=None, env=None)
    CommHelper(input_api, ['pyyyyython', '-m', 'test_module'],
                    ret=(('foo', None), 1), cwd=None, env=None)
    self.assertEquals('test_module failed\nfoo', results[0]._message)
    CommHelper(input_api, ['pyyyyython', '-m', 'test_module'],
                    ret=(('foo', None), 1), cwd=None, env=None)
    self.assertEquals('test_module failed\nfoo', results[0]._message)
    CommHelper(input_api, ['pyyyyython', '-m', 'test_module'],
                    cwd=None, env=None)
    CommHelper(input_api,
        ['pyyyyython', pylint, '--args-on-stdin'],
        env=mox.IgnoreArg(), stdin='file1.py\n--rcfile=%s' % pylintrc)
    self.checkstdout('')
                           uncovered_files=set(['foo/xyz.cc', 'foo/bar.cc']),
                                           'for these files:\n'
                                           '    foo/bar.cc\n'
                                           '    foo/xyz.cc\n',
    CommHelper(input_api, ['allo', '--verbose'], cwd=self.fake_root_dir)
    CommHelper(input_api, cmd, cwd=self.fake_root_dir, ret=(('', None), 1))
    CommHelper(
        input_api,