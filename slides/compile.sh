# packages needed:
# pandoc
# texlive
# texlive-xetex
# texlive-lang-cyrillic
# graphviz
# librsvg2-bin

pandoc ${1}.md -t beamer -o ${1}.pdf --pdf-engine=xelatex --lua-filter diagram.lua --slide-level=2 
