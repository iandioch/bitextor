
bitextordir = $(prefix)/share/bitextor

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = bitextor-git.pc

SUBDIRS= utils ulysses piped-boilerpipe piped-tika ulysses-data model

bitextor_SOURCEFILES=bitextor.sh bitextor-align-documents.py bitextor-align-segments.py \
            bitextor-cleantextalign.py bitextor-crawl2ett.sh bitextor-rank.py bitextor-train-document-alignment.py \
            bitextor-ett2lett.sh bitextor-idx2ridx.py bitextor-lett2idx.py tar2lett.py \
            bitextor-lett2lettr.py bitextor-ridx2filenames.py bitextor-crawl.py bitextor-downloadweb.sh bitextor-webdir2ett.sh \
            bitextor-buildTMX.sh bitextor-score-document-alignment.py bitextor-builddics.sh install_nltk_data.py \
            features/bitextor-structuredistance.py features/bitextor-urlsetoverlap.py features/bitextor-urlsdistance.py \
            features/bitextor-imagesetoverlap.py features/bitextor-mutuallylinked.py features/bitextor-urlscomparison.py

bin_SCRIPTS=bitextor bitextor-align-documents bitextor-align-segments bitextor-cleantextalign bitextor-rank \
            bitextor-ett2lett bitextor-crawl bitextor-train-document-alignment tar2lett \
            bitextor-idx2ridx bitextor-lett2idx bitextor-lett2lettr bitextor-builddics bitextor-crawl2ett bitextor-downloadweb bitextor-webdir2ett \
            bitextor-ridx2filenames bitextor-buildTMX bitextor-score-document-alignment bitextor-elrc-filtering \
            features/bitextor-structuredistance features/bitextor-urlsetoverlap features/bitextor-urlsdistance \
            features/bitextor-imagesetoverlap features/bitextor-mutuallylinked features/bitextor-urlscomparison 
            
bitextor_MANS=doc/bitextor.1 doc/bitextor-cleantextalign.1 \
         doc/bitextor-distancefilter.1 doc/bitextor-ett2lett.1 \
         doc/bitextor-idx2ridx.1 doc/bitextor-lett2idx.1 doc/bitextor-lett2lettr.1 \
         doc/bitextor-buildTMX.1


EXTRA_DIST= $(bitextor_MANS) $(bitextor_SOURCEFILES) utils \
            model

CLEANFILES=$(bin_SCRIPTS)

compile-smttools:
	cd mgiza/mgizapp/ && cmake . && make

compile-hunalign:
	cd hunalign/src/hunalign && make 

install-smttools:
	cp mgiza/mgizapp/bin/* $(prefix)/bin/.
	cp clustercat/bin/* $(prefix)/bin/.
	cp textsanitizer.py $(prefix)/bin/.
	touch $(prefix)/bin/__init__.py

install-hunalign:
	cp hunalign/src/hunalign/hunalign $(prefix)/bin/.

bitextor-train-document-alignment: bitextor-train-document-alignment.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

install: install-recursive install-smttools install-hunalign

bitextor: bitextor.sh compile-smttools compile-hunalign
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__WC__!$(WC)!g" | \
	sed "s!__GREP__!$(GREP)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@

nltk_data:
	python install_nltk_data.py

features/bitextor-urlscomparison: features/bitextor-urlscomparison.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

features/bitextor-structuredistance: features/bitextor-structuredistance.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

features/bitextor-mutuallylinked: features/bitextor-mutuallylinked.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-rank: bitextor-rank.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

features/bitextor-urlsetoverlap: features/bitextor-urlsetoverlap.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

features/bitextor-imagesetoverlap: features/bitextor-imagesetoverlap.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

features/bitextor-urlsdistance: features/bitextor-urlsdistance.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-crawl: bitextor-crawl.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-crawl2ett: bitextor-crawl2ett.sh
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__BASH__!$(BASH)!g" | \
	sed "s!__JAVA__!$(JAVA)!g" | \
	sed "s!__GAWK__!$(GAWK)!g" | \
	sed "s!__GREP__!$(GREP)!g" | \
	sed "s!__WC__!$(WC)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" >$@

bitextor-buildTMX: bitextor-buildTMX.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-ridx2filenames: bitextor-ridx2filenames.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-align-segments: bitextor-align-segments.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHONPATH__!$(pythondir)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" | \
        sed "s!__BASH__!$(BASH)!g;" >$@

bitextor-score-document-alignment: bitextor-score-document-alignment.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHONPATH__!$(pythondir)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-align-documents: bitextor-align-documents.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-cleantextalign: bitextor-cleantextalign.py
	sed "s!__ENV__!$(ENV)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" >$@

bitextor-ett2lett: bitextor-ett2lett.sh
	sed "s!__BASH__!$(BASH)!g" $< | \
	sed "s!__JAVA__!$(JAVA)!g" | \
	sed "s!__WC__!$(WC)!g" | \
	sed "s!__PREFIX__!$(prefix)!g" | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" >$@

bitextor-idx2ridx: bitextor-idx2ridx.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" >$@

bitextor-lett2idx: bitextor-lett2idx.py nltk_data
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@

bitextor-lett2lettr: bitextor-lett2lettr.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__ENV__!$(ENV)!g" >$@

bitextor-builddics: bitextor-builddics.sh nltk_data
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@

bitextor-elrc-filtering: bitextor-elrc-filtering.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@	

bitextor-downloadweb: bitextor-downloadweb.sh
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@ 

bitextor-webdir2ett: bitextor-webdir2ett.sh
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@

tar2lett: tar2lett.py
	sed "s!__PREFIX__!$(prefix)!g" $< | \
	sed "s!__ENV__!$(ENV)!g" | \
	sed "s!__PYTHON__!$(PYTHON)!g" | \
	sed "s!__BASH__!$(BASH)!g;" >$@

