import subprocess
from typing import List, Tuple
from parse import parse
from pprint import pprint
import time

def _parse_level(output: str) -> 'LevelStats':
    lines = output.splitlines()
    stats_string = '&'.join(lines[-5:][:-1])
    stats = parse("total of {patterns:d} patterns at hyph_level {level:d}&hyphenate word list? writing pattmp.{:d}& &{good:d} good, {bad:d} bad, {missed:d} missed", stats_string).named
    return LevelStats(stats["patterns"], stats["level"],stats["good"],stats["bad"],stats["missed"])

def _parse_params(parfile):
    hyph_start_finish = {}
    pat_start_finish = {}
    good_bad_thres = {}
    exec(open(parfile).read())
    return (pat_start_finish, good_bad_thres)

def train(directory, parfile, makeargs="", output_markdown=True) -> List["LevelStats"]:
    """Make patterns with the given parfile and makeargs. 
    Supply a parameter name like liang, not out/liang.par or out/liang.
    Patterns will be trained on wordlist specified in the Make variable WORDLISTTOUSE."""

    ts = time.time()
    subprocess.check_output("cd "+directory+"; rm out/"+parfile+".pat; nice make "+makeargs+" -s out/"+parfile+".pat", shell=True, stderr=subprocess.STDOUT)
    took = time.time() - ts 

    levels = []
    for run in range(1,8):
        try:
            with open(directory+"/out/pattern."+str(run)+".log") as f:
                levels.append(_parse_level(f.read()))
        except IOError as e:
            if run != 1:
                break
            else:
                raise e
    if output_markdown:
        pat_start_finish, good_bad_thres = _parse_params(directory+"/out/"+parfile+".par")
        return _format_training_output(levels, parfile, took, pat_start_finish, good_bad_thres)
    else:
        return levels
    
def show_stats(pattern, directory=".") -> str:
    md = "## Pattern "+pattern+"\n\n"
    lines, kbytes = _get_pattern_stats(directory, pattern)
    md += lines+" patterns, "+str(kbytes)+" kB\n"
    return md

def validate(directory, pattern) -> str:
    """Run validation of a given pattern and output a md-formatted summary.
    
    Makes pattern from parameters if not yet made.

    Supply pattern like liang, not liang.pat nor out/liang."""

    try:
        subprocess.check_output("cd "+directory+"; make -s out/"+pattern+".wleval", shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e
    with open(directory+"/out/"+pattern+".wleval") as f:
        stats = "\n".join(f.read().splitlines()[-3:])
    
    md = "## Pattern "+pattern+"\n\n"
    lines, kbytes = _get_pattern_stats(directory, pattern)
    md += lines+" patterns, "+str(kbytes)+" kB\n"
    md += stats

    return md

def _get_pattern_stats(directory, pattern) -> Tuple[str, int]:
    wcl = subprocess.check_output(["wc", "-l", directory+"/out/"+pattern+".pat"]).decode('utf-8')
    wcc = subprocess.check_output(["wc", "-c", directory+"/out/"+pattern+".pat"]).decode('utf-8')

    lines = wcl.split(" ")[0]
    kbytes = int(int(wcc.split(" ")[0])/1024)

    return (lines, kbytes)

def _format_training_output(levels: List['LevelStats'], param: str, secs: float, pat_start_finish: str, good_bad_thres: str) -> str:
    md = "## "+param+"\n\n"
    md += "Took: "+str(round(secs,2))+" seconds\n\n"
    md += "Level|Patterns|Good|Bad|Missed|Length|Param\n"
    md += "---|---|---|---|---|---|---\n"
    i = 1
    for l in levels:
        md += "{} | {} | {} | {} | {} | {} | {}\n".format(l.level, l.patterns, l.good, l.bad, l.missed, pat_start_finish[i], good_bad_thres[i])
        i += 1
    return md

class LevelStats():
    """Represents the output of one patgen invocation."""

    def __init__(self, patterns, level, good, bad, missed):
        self.patterns = patterns
        self.level = level
        self.good = good
        self.bad = bad
        self.missed = missed

if __name__ == '__main__':
    pprint(validate("../czhyphen2","liang"))