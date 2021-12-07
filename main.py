# write out xml for bibliography containing only references used in the manuscript.

# WARNING: bibtexparser does not find entries labelled 'software'

import bibtexparser
import os
import sys

path = 'C:/Users/sfon036/Desktop/work_files/PhysiomeSubmissions/TEX_submission_folders/S000001/'
try:
    bibfile = [f for f in os.listdir(path) if f.endswith('.bib')][0]
except:
    sys.exit(".bib file is missing")
try:
    bblfile = [f for f in os.listdir(path) if f.endswith('.bbl')][0]
except:
    sys.exit(".bbl file is missing")


with open(path+bibfile) as f:
    bib_database = bibtexparser.load(f)

# parse the bbl file to write out only sources that are cited in the manuscript
used_sources = []
with open(path+bblfile) as bl:
    for line in bl:
        if 'bibitem' in line:
            multiline = False
            refTitle = line
            # append to line with continuation of ref title, which could br broken onto several lines
            while '}' not in line:
                multiline = True
                line = bl.readline()
                refTitle += line
            if multiline:
                refTitle += line
            key = refTitle.split('{')[-1].split('}')[0]
            used_sources.append(key)

# write out title, journal_title, author, volume, issue year
xr_list = ['article_title', 'journal_title', 'author', 'volume', 'issue', 'cYear']
bib_list = ['title', 'journal', 'author', 'volume', 'issue', 'year']
fields = dict()
fields = {xr_list[i]: bib_list[i] for i in range(len(xr_list))}

XR_output = path + 'crossref_citation_list.xml'
with open(XR_output, 'w') as w:
    w.write('<citation_list>\n')
    for count, entry in enumerate(bib_database.entries):
        if entry['ID'] in used_sources:
            w.write('<citation key='+str(count)+'>\n',)
            for field in fields:
                try:
                    w.write('\t<%s>' % field + entry['%s' % fields[field]] + '</%s>\n' % field)
                except:
                    pass
            w.write('/<citation>\n')
    w.write('/<citation_list>\n')
