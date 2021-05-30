"""
#############################################################################
#                                FORMAT BIBTEX                              #
#############################################################################
Author:     Mohammad Hossain Mohammadi
Date:       November 2017
"""""

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def format_bibtex(pub, format, main_author, initials):
    """
    Format a publication dictionary in a required formatting style
    Args:       -pub is a publication data structure constaining Bibtex fields
                -format is a string for the format required, e.g. 'jemdoc', 'tex', 'html'
                -main_author is a string of the main author's last name
                -initials controls whether the first names are shown as initials {0/1}
    Returns:    -ref is a string of the publication reference
                -entry_type is a string for the Bibtex publication entrytype
                -year is an integer for the publication year (useful for sorting)
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Initialization
    ref = ''
    entry_type = pub["ENTRYTYPE"]
    authors = ''
    title = ''
    journal = ''
    booktitle = ''
    publisher = ''
    school = ''
    address = ''
    volume = ''
    number = ''
    pages = ''
    month = ''
    year = ''
    doi = ''
    link = ''
    institution = ''
    note = ''

    # Set Bibtex Values if Existing in Pub Dictionary
    # if entry_type == 'article' or entry_type == 'inproceedings' or entry_type == 'incollection':
        # if 'month' in pub:     # e.g. Jan. for January
            # month = pub["month"][0:3] + '.'
    if 'doi' in pub:
        doi = pub["doi"]
    if 'address' in pub:
        address = pub["address"]
    if 'title' in pub:
        title = pub["title"]
    if 'publisher' in pub:
        publisher = pub["publisher"]
    if 'year' in pub:
        year = pub["year"]
    if 'volume' in pub:
        volume = pub["volume"]
    if 'pages' in pub:
        pages = pub["pages"]
    if 'number' in pub:
        number = pub["number"]
    if 'journal' in pub:
        journal = pub["journal"]
    if 'booktitle' in pub:
        booktitle = pub["booktitle"]
    if 'link' in pub:
        link = pub["link"]
    if 'school' in pub:
        school = pub["school"]
    if 'institution' in pub:
        institution = pub["institution"]
    if 'note' in pub:
        note = pub["note"]

    # Format Author Names based on Formatting Style
    authors_ = pub["author"].split(' and ')
    for iA, author_ in enumerate(authors_):
        if ',' in author_:  # Order: LastName, FirstName
            anames = author_.split(', ')
            fname = anames[1]           # First name string
            lname = anames[0]           # Last name string
        else:               # Order: FirstName LastName
            anames = author_.split(' ')
            lname = anames[-1]          # Last name string
            fname = anames[:-1]         # First name string
            fname = ' '.join(fname)

        # Convert first name into initials (if not already)
        if initials==1 and ('.' not in fname):
            fnames = fname.split(' ')
            fname = ''
            for iF,fn in enumerate(fnames):
                fname = fname + fn[0] + '.'     # Full stop & space after initials
                if iF<(len(fnames)-1):
                    fname += ' '                # Space b/w author's first names

        # Boldify main author (depends on formatting style)
        author = fname + ' ' + lname
        if main_author == lname:
            if format == 'jemdoc':
                author = '*' + author + '*'
            elif format == 'tex':
                author = '\\textbf{' + author + '}'
            elif format == 'html':
                author = '<strong>' + author + '</strong>'

        # Combine author list into 1 string
        authors += author
        if iA<(len(authors_)-2):
            authors += ', '     # Separation b/w author full names
        elif iA==(len(authors_)-2):
            authors += ', and '  # Separation for last author

    # Format Other Bibtex Fields based on Formatting Style
    if format == 'jemdoc':
        title = '"*' + title + '*,"'
        journal = '/' + journal + '/'
        booktitle = '/' + booktitle + '/'
        doi = '[https://doi.org/' + doi + ' DOI:' + doi + ']'
        link = '[' + link + ' Link]'
        institution = '/' + institution + '/'
    elif format == 'tex':
        title = '``' + title + ',\'\''
        journal = '\\textit{' + journal + '}'
        booktitle = '\\textit{' + booktitle + '}'
        doi = '\\href{https://doi.org/' + doi + '}{DOI:' + doi + '}'
        link = '\\href{' + link + '}{Link}'
        institution = '\\textit{' + institution + '}'
    elif format == 'html':
        title = '<em>' + title + '</em>'
        journal = '<em>' + journal + '</em>'
        booktitle = '<em>' + booktitle + '</em>'
        doi = '<a href="https://doi.org/' + doi + '">' + doi + '</a>'
        link = '<a href="' + link + '">link</a>'

    # Create Reference based on Formatting Style
    if entry_type == 'book':
        ref = authors + '. ' + title + ' ' + address + ': ' + publisher + ', ' + year + '.'
    elif entry_type == 'article':
        ref = authors + ', ' + title + ' ' + journal + ', Vol. ' + volume + ', No. ' + number + ', pp. ' + pages + ', ' + year + '. \\n' + doi
    elif entry_type == 'inproceedings' or entry_type == 'incollection':
        ref = authors + ', ' + title + ' ' + booktitle + ', ' + address + ', ' + month + ' ' + year + '. \\n' + doi
    elif entry_type == 'mastersthesis':
        ref = authors + ', ' + title + ' Master\'s Thesis, ' + school + ', ' + address + ', ' + year + '. \\n' + link
    elif entry_type == 'phdthesis':
        ref = authors + ', ' + title + ' PhD Dissertation, ' + school + ', ' + address + ', ' + year + '. \\n' + link
    elif entry_type == 'techreport':
        ref = authors + ', ' + title + ' ' + institution + ', ' + number + ', ' + month + ' ' + year + '.'
    elif entry_type == 'misc':
        ref = authors + ', ' + title + ' ' + note + '. \\n' + link

    return ref, entry_type, int(year)


def create_research_file(db, format, outname, main_author, initials):
    """
    Creates a file of research publications
    Args:       -db is the publication data structure containing Bibtex fields
                -format is a string for the format required, e.g. 'jemodoc', 'tex', 'html'
                -outname is a string for the output file name, e.g. 'research'
                -main_author is the main author's last name string
                -initials controls whether the first names are shown as initials {0/1}
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Sorting Key
    def access_year(elem):
        return elem[2]

    # Initialization
    books = []
    journals = []
    conferences = []
    koreanconferences = []
    theses = []
    techreports = []
    patents = []

    # Create Separate Lists for Publication Type
    for pub in db.entries:
        # Format publication dictionary using a formatting style
        ref, entry_type, year = format_bibtex(pub, format, main_author, initials)

        # Append publication reference into lists
        if entry_type == 'book':
            books.append([ref, entry_type, year])
        elif entry_type == 'article':
            journals.append([ref, entry_type, year])
        elif entry_type == 'inproceedings':
            conferences.append([ref, entry_type, year])
        elif entry_type == 'incollection':
            koreanconferences.append([ref, entry_type, year])
        elif entry_type == 'mastersthesis' or entry_type == 'phdthesis':
            theses.append([ref, entry_type, year])
        elif entry_type == 'misc':
            patents.append([ref, entry_type, year])

    # Create Sorted Research File
    outfile = outname + '.' + format
    with open(outfile, 'w') as the_file:
        if format == 'jemdoc':
            the_file.write('# jemdoc: menu{MENU}{'+ outname + '.html}, notime\n')
            the_file.write('= Publications\n\n')
            the_file.write('*[https://scholar.google.co.uk/citations?user=DhdeDm8AAAAJ Google Scholar]*\n\n')

            # if books:
            #     books.sort(reverse=True, key=access_year)
            #     the_file.write('== Books\n')
            #     for book in books:
            #         the_file.write('. ' + book[0] + '\n')
            #     the_file.write('\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('== Dissertation\n')
                for thesis in theses:
                    the_file.write('. ' + thesis[0] + '\n')
                the_file.write('\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('== Journal\n')
                for journal in journals:
                    the_file.write('. ' + journal[0] + '\n')
                the_file.write('\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('== Conference\n')
                for conference in conferences:
                    the_file.write('. ' + conference[0] + '\n')
                the_file.write('\n')

            if techreports:
                techreports.sort(reverse=True, key=access_year)
                the_file.write('== Technical Report\n')
                for techreport in techreports:
                    the_file.write('. ' + techreport[0] + '\n')
                the_file.write('\n')

            if koreanconferences:
                koreanconferences.sort(reverse=True, key=access_year)
                the_file.write('== National Conference\n')
                for koreanconference in koreanconferences:
                    the_file.write('. ' + koreanconference[0] + '\n')
                the_file.write('\n')

            if patents:
                patents.sort(reverse=True, key=access_year)
                the_file.write('== Patent\n')
                for patent in patents:
                    the_file.write('. ' + patent[0] + '\n')
                the_file.write('\n')



        elif format == 'tex':
            if books:
                books.sort(reverse=True, key=access_year)
                the_file.write('\\section{BOOKS}\n\n')
                for book in books:
                    the_file.write(book[0] + '\n\n')
                the_file.write('\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('\\section{JOURNALS}\n\n')
                for journal in journals:
                    the_file.write(journal[0] + '\n\n')
                the_file.write('\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('\\section{CONFERENCES}\n\n')
                for conference in conferences:
                    the_file.write(conference[0] + '\n\n')
                the_file.write('\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('\\section{THESES}\n\n')
                for thesis in theses:
                    the_file.write(thesis[0] + '\n\n')
                the_file.write('\n')

        elif format == 'html':
            the_file.write('<!-- Question -->\n')
            the_file.write('<div class="panel panel-default">\n')
            the_file.write('\t<div class="panel-heading">\n')
            the_file.write('\t<h4 class="panel-title">\n')
            the_file.write('\t<a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion1" href="#collapse' + bibname + '">\n')
            the_file.write('\t' + bibname + ' Calendar Year\n')
            the_file.write('\t</a>\n')
            the_file.write('\t</h4>\n')
            the_file.write('\t</div>\n')
            the_file.write('\t<!-- Answer -->\n')
            the_file.write('\t<div id="collapse' + bibname + '" class="panel-collapse collapse">\n')
            the_file.write('\t\t<div class="panel-body">\n')

            if books:
                books.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Book publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for book in books:
                    the_file.write('\t\t\t<li>' + book[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            if journals:
                journals.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Journal publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for journal in journals:
                    the_file.write('\t\t\t<li>' + journal[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            if conferences:
                conferences.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Conference publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for conference in conferences:
                    the_file.write('\t\t\t<li>' + conference[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            if theses:
                theses.sort(reverse=True, key=access_year)
                the_file.write('\t\t<u><strong>Thesis publications:</strong></u><br/>\n')
                the_file.write('\t\t<ol>\n')
                for thesis in theses:
                    the_file.write('\t\t\t<li>' + thesis[0] + '</li><br>\n')
                the_file.write('\t\t</ol>\n')

            the_file.write('\t\t</div>\n')
            the_file.write('\t</div>\n')
            the_file.write('</div>\n')


def main(format, bibname, outname, main_author, initials):
    """
    Format publication references in a formatting style
    Args:       -format is a string for the format required, e.g. jemodoc, tex, html
                -bibname is the Bibtex file name without any extension, e.g. MHM
                -outname is a string for the output file name, e.g. research
                -main_author is a string of the main author's last name used for bolding, e.g. Mohammadi or ""
                -initials is an integer which controls whether the first names are shown as initials {0/1}
    Author:     Mohammad Hossain Mohammadi
    Date:       November 2017
    """""
    # Load Bibtex File
    with open(bibname + ".bib") as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        db = bibtexparser.load(bibtex_file, parser=parser)

    # Creates a Research File of Publication References
    create_research_file(db, format, outname, main_author, initials)


# Handle Arguments & Call Main Function
if __name__ == '__main__':
    format = str(sys.argv[1])
    bibname = str(sys.argv[2])
    outname = str(sys.argv[3])
    main_author = str(sys.argv[4])
    initials = int(sys.argv[5])

    sys.exit(main(format, bibname, outname, main_author, initials))
