# write out xml for bibliography containing only references used in the manuscript.

# WARNING: bibtexparser does not find entries labelled 'software'

# Requires local compilation of .tex and .bib files, in order to access the .bbl file.

import bibtexparser
import os
import sys

parent_path = 'C:/Users/sfon036/Desktop/work_files/PhysiomeSubmissions/TEX_submission_folders/'
subs = [f for f in os.listdir(parent_path) if 'originals' not in f]
subs = ['S000014']

for sub in subs:
    path = parent_path+sub+'/'
    submissionID = path.split('/')[-2]
    # path = 'examples/'
    # submissionID = "S000012"

    # find DOI of this article
    DOI = []
    pub_path = "C:/Users/sfon036/Documents/physiome_curation_work/journal-website/content/Articles/"
    # pub_path = path
    with open(pub_path+submissionID+'.md') as p:
        for line in p:
            if "DOI:" in line:
                DOI = line.split(':')[-1] #DOI = "10.36903/physiome.16590317"
                break
    if not DOI:
        sys.exit("DOI is missing")

    try:
        bibfile = [f for f in os.listdir(path) if f.endswith('.bib')][0]
    except:
        sys.exit(".bib file is missing")
    try:
        bblfile = [f for f in os.listdir(path) if f.endswith('.bbl')][0]
    except:
        sys.exit(".bbl file is missing")


    #  all fields in .bib file must be enclosed with curly braces {} after the equals sign
    with open(path+bibfile, encoding="utf8") as f:
        with open(path+'tempbib.bib','w',encoding="utf8") as w:
            for line in f:
                if 'month' in line and '{' not in line:
                    line = 'month = {' + line.split('=')[-1].replace(',','') + '},'#month = dec,
                w.write(line)

    with open(path+'tempbib.bib', encoding="utf8") as f:
        bib_database = bibtexparser.load(f)

    # parse the bbl file to write out only sources that are cited in the manuscript
    used_sources = []
    with open(path+bblfile, encoding="utf8") as bl:
        for line in bl:
            if 'bibitem' in line:
                multiline = False
                refTitle = line
                # append to line with continuation of ref title, which could br broken onto several lines
                while '}\n' not in line:
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

    preamble = "<doi_batch version=\"4.4.2\" xmlns=\"http://www.crossref.org/doi_resources_schema/4.4.2\"\
      xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n\
      xsi:schemaLocation=\"http://www.crossref.org/doi_resources_schema/4.4.2 http://www.crossref.org/schemas/doi_resources4.4.2.xsd\">\n\
    <head>\n\
    <doi_batch_id>%s_addition1</doi_batch_id>\n\
    <depositor>\n\
    <depositor_name>Shelley Fong</depositor_name>\n\
    <email_address>s.fong@auckland.ac.nz</email_address>\n\
    </depositor>\n\
    </head>\n\
    <body>\n\
    <doi_citations>\n\
    <!--  ******* The DOI of the article *******   -->\n\
    <doi>%s</doi>\n" %(submissionID, DOI)

    XR_output = path + submissionID + '_with_citation_list.xml'
    count = 0
    with open(XR_output, 'w') as w:
        w.write(preamble)
        w.write('<citation_list>\n')
        for entry in bib_database.entries:
            if entry['ID'] in used_sources:
                w.write('<citation key="ref'+str(count)+'">\n',)
                try:
                    if entry['author'] == 'MATLAB':
                        del entry['author']
                        entry['title'] = 'MATLAB ' + entry['title']
                except:
                    pass
                for field in fields:
                    try:
                        w.write('\t<%s>' % field + entry['%s' % fields[field]] + '</%s>\n' % field)
                    except:
                        pass
                count += 1
                w.write('</citation>\n')
        w.write('</citation_list>\n')
        w.write('</doi_citations>\n')
        print('Written out ' + XR_output)

    plaintext_output = path + submissionID + '_PLAINTEXT_citation_list.xml'
    count = 1
    with open(plaintext_output, 'w') as po:
        po.write('References: ')
        for entry in bib_database.entries:
            if entry['ID'] in used_sources:
                po.write(str(count)+'. ')
                for f, field in enumerate(fields):
                    if 'article_title' in field or 'author' in field:
                        try:
                            po.write(entry['%s' % fields[field]] + '. ')
                        except:
                            pass
                    else:
                        try:
                            po.write(bib_list[f].capitalize() + ': '+ entry['%s' % fields[field]]+'. ')
                        except:
                            pass
                po.write(' <br />')
                # po.write('\n\n')
                count += 1
        print('Written out ' + plaintext_output)
