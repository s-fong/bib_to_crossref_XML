
import bibtexparser

path = 'examples/'
with open(path+'sample.bib') as f:
    bib_database = bibtexparser.load(f)


# write out title, journal_title, author, volume, issue year
xr_list = ['article_title', 'journal_title', 'author', 'volume', 'issue', 'cYear']
bib_list = ['title', 'journal', 'author', 'volume', 'issue', 'year']
fields = dict()
fields = {xr_list[i]: bib_list[i] for i in range(len(xr_list))}

XR_output = path + 'crossref_citation_list.xml'
with open(XR_output, 'w') as w:
    w.write('<citation_list>\n')
    for count, entry in enumerate(bib_database.entries):
        w.write('<citation key='+str(count)+'>\n',)
        for field in fields:
            try:
                w.write('\t<%s>' % field + entry['%s' % fields[field]] + '</%s>\n' % field)
            except:
                pass
        w.write('/<citation>\n')
    w.write('/<citation_list>\n')
