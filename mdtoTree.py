from markdown_it import MarkdownIt
from rich.tree import Tree

def build_tree(tokens, parent):
    stack = [parent]
    for token in tokens:
        if token.type in ("heading_open", "list_item_open", "paragraph_open"):
            node = stack[-1].add(f"[bold]{token.tag}[/bold]")
            stack.append(node)
        elif token.type in ("heading_close", "list_item_close", "paragraph_close"):
            stack.pop()
        elif token.type == "inline":
            stack[-1].add(token.content)

def markdown_to_tree(md_text):
    md = MarkdownIt()
    tokens = md.parse(md_text)
    root = Tree("Markdown Document")
    build_tree(tokens, root)
    return root

# Example usage:
md_text = r"""# Article Title  

First Author $^{1,2}$ \*, Second Author $^{2,3}$ † and Third Author $^{1,2}$ †  

1\*Department, Organization, Street, City, 100190, State, Country.   
$^2$ Department, Organization, Street, City, 10587, State, Country.   
$^3$ Department, Organization, Street, City, 610101, State, Country.  

$^*$ Corresponding author(s). E-mail(s): iauthor@gmail.com; Contributing authors: iiauthor@gmail.com; iiiauthor@gmail.com; †These authors contributed equally to this work.  

Abstract  

The abstract serves both as a general introduction to the topic and as a brief, non-technical summary of the main results and their implications. Authors are advised to check the author instructions for the journal they are submitting to for word limits and if structural elements like subheadings, citations, or equations are permitted.  

Keywords: keyword1, Keyword2, Keyword3, Keyword4  

## 1 Introduction  

The Introduction section, of referenced text [1] expands on the background of the work (some overlap with the Abstract is acceptable). The introduction should not include subheadings.  

Springer Nature does not impose a strict layout as standard however authors are advised to check the individual requirements for the journal they are planning to submit to as there may be journal-level preferences. When preparing your text please also be aware that some stylistic choices are not supported in full text XML (publication version), including coloured font. These will not be replicated in the typeset article if it is accepted.  

## 2 Results  

Sample body text. Sample body text. Sample body text. Sample body text.   
Sample body text. Sample body text. Sample body text. Sample body text.  

## 3 This is an example for first level head—section head  

3.1 This is an example for second level head—subsection head  

3.1.1 This is an example for third level head—subsubsection head  

Sample body text. Sample body text. Sample body text. Sample body text.   
Sample body text. Sample body text. Sample body text. Sample body text.  

## 4 Equations  

Equations in LATEX can either be inline or on-a-line by itself (“display equations”). For inline equations use the $\$.23$ commands. E.g.: The equation $H\psi=E\psi$ is written via the command $\$123,456,789$ .  

For display equations (with auto generated equation numbers) one can use the equation or align environments:  

$$
\|\tilde{X}(k)\|^{2}\leq\frac{\displaystyle\sum_{i=1}^{p}\left\|\tilde{Y}_{i}(k)\right\|^{2}+\displaystyle\sum_{j=1}^{q}\left\|\tilde{Z}_{j}(k)\right\|^{2}}{p+q}.
$$  

where,  

$$
\begin{array}{l}{{\displaystyle D_{\mu}=\partial_{\mu}-i g\frac{\lambda^{a}}{2}A_{\mu}^{a}}}\\ {{\displaystyle F_{\mu\nu}^{a}=\partial_{\mu}A_{\nu}^{a}-\partial_{\nu}A_{\mu}^{a}+g f^{a b c}A_{\mu}^{b}A_{\nu}^{a}}}\end{array}
$$  

Notice the use of \nonumber in the align environment at the end of each line, except the last, so as not to produce equation numbers on lines where no equation numbers are required. The \label{} command should only be used at the last line of an align environment where \nonumber is not used.  

$$
Y_{\infty}=\left({\frac{m}{\mathrm{GeV}}}\right)^{-3}\left[1+{\frac{3\ln(m/\mathrm{GeV})}{15}}+{\frac{\ln(c_{2}/5)}{15}}\right]
$$  

The class file also supports the use of \mathbb{}, \mathscr{} and \mathcal{} commands. As such \mathbb{R}, \mathscr{R} and \mathcal{R} produces $\mathbb{R}$ , $\mathcal{R}$ and $\mathcal{R}$ respectively (refer Subsubsection 3.1.1).  

## 5 Tables  

Tables can be inserted via the normal table and tabular environment. To put footnotes inside tables you should use \footnotetext[]{...} tag. The footnote appears just below the table itself (refer Tables 1 and 2). For the corresponding footnotemark use \footnotemark[...]  

Table 1 Caption text   


<html><body><table><tr><td>Column 1</td><td>Column 2</td><td>Column 3</td><td>Column 4</td></tr><tr><td>row 1</td><td>data 1</td><td>data 2</td><td>data 3</td></tr><tr><td>row 2</td><td>data 4</td><td>data 51</td><td>data 6</td></tr><tr><td>row 3</td><td>data 7</td><td>data 8</td><td>data 92</td></tr></table></body></html>

Source: This is an example of table footnote. This is an example of table footnote. 1Example for a first table footnote. This is an example of table footnote. 2Example for a second table footnote. This is an example of table footnote.  

The input format for the above table is as follows:  

\begin{table}[<placement-specifier>]   
\begin{center}   
\begin{minipage}{<preferred-table-width>}   
\caption{<table-caption>}\label{<table-label>}%   
\begin{tabular}{@{}llll@{}}   
\toprule   
Column 1 & Column 2 & Column 3 & Column 4\\   
\midrule   
row 1 & data 1 & data 2 & data 3 \\   
row 2 & data 4 & data 5\footnotemark[1] & data 6 \\   
row 3 & data 7 & data 8 & data 9\footnotemark[2]\\   
\botrule   
\end{tabular}   
\footnotetext{Source: This is an example of table footnote. This is an example of table footnote.}   
\footnotetext[1]{Example for a first table footnote.   
This is an example of table footnote.}   
\footnotetext[2]{Example for a second table footnote. This is an example of table footnote.}   
\end{minipage}   
\end{center}   
\end{table}  

Springer Nature 2021 LATEX template  

Table 2 Example of a lengthy table which is set to full textwidth   


<html><body><table><tr><td></td><td colspan="3">Element 11</td><td colspan="3">Element 22</td></tr><tr><td>Project</td><td>Energy</td><td>Ocalc</td><td>Oexpt</td><td>Energy</td><td>Ocalc</td><td>Oexpt</td></tr><tr><td>Element 3</td><td>990A</td><td>1168</td><td>1547 ± 12</td><td>780 A</td><td>1166</td><td>1239 ± 100</td></tr><tr><td>Element 4</td><td>500A</td><td>961</td><td>922 ± 10</td><td>900A</td><td>1268</td><td>1092 ± 40</td></tr></table></body></html>

1Example for a first table footnote. 2Example for a second table footnote.  

Note: This is an example of table footnote. This is an example of table footnote this is an example of table footnote this is an example of table footnote this is an example of table footnote.  

In case of double column layout, tables which do not fit in single column width should be set to full text width. For this, you need to use \begin{table\*} ... \end{table\*} instead of \begin{table} . \end{table} environment. Lengthy tables which do not fit in textwidth should be set as rotated table. For this, you need to use \begin{sidewaystable} .. \end{sidewaystable} instead of \begin{table\*} ... \end{table\*} environment. This environment puts tables rotated to single column width. For tables rotated to double column width, use \begin{sidewaystable\*} . \end{sidewaystable\*}.  

## 6 Figures  

As per the LATEX standards you need to use eps images for LATEX compilation and pdf/jpg/png images for PDFLaTeX compilation. This is one of the major difference between LATEX and PDFLaTeX. Each image should be from a single input .eps/vector image file. Avoid using subfigures. The command for inserting images for LATEX and PDFLaTeX can be generalized. The package used to insert images in LaTeX/PDFLaTeX is the graphicx package. Figures can be inserted via the normal figure environment as shown in the below example:  

\begin{figure}[<placement-specifier>]   
\centering   
\includegraphics{<eps-file>}   
\caption{<figure-caption>}\label{<figure-label>}   
\end{figure}  

In case of double column layout, the above format puts figure captions/images to single column width. To get spanned images, we need to provide \begin{figure\*} ... \end{figure\*}.  

For sample purpose, we have included the width of images in the optional argument of \includegraphics tag. Please ignore this.  

Table 3 Tables which are too long to fit, should be written using the “sidewaystable” environment as shown here   


<html><body><table><tr><td rowspan="6"></td><td></td><td></td></tr><tr><td></td><td>A Ａ AA 084 006</td></tr><tr><td></td><td>dxa o F 776</td></tr><tr><td></td><td>196</td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr></table></body></html>

Note: This is an example of table footnote this is an example of table footnote this is an example of table footnote this is anexample of table footnote this is an example of table footnote.   
1This is an example of table footnote.  

![](images/90af867b7ff8aa85c2ddca16574be0754670bd4f569a18b0aeb15264b0c2f837.jpg)  
Fig. 1 This is a widefig. This is an example of long caption this is an example of long caption this is an example of long caption this is an example of long caption  

## 7 Algorithms, Program codes and Listings  

Packages algorithm, algorithmicx and algpseudocode are used for setting algorithms in LATEX using the format:  

\begin{algorithm}   
\caption{<alg-caption>}\label{<alg-label>}   
\begin{algorithmic}[1]   
\end{algorithmic}   
\end{algorithm}  

You may refer above listed package documentations for more details before setting algorithm environment. For program codes, the “program” package is required and the command to be used is \begin{program} .. \end{program}. A fast exponentiation procedure:  

begin for $i:=1$ to 10 step 1 do $\mathsf{e x p t}(2,i)$ ; newline() od Comments will be set flush to the right margin   
where   
proc $\mathsf{e x p t}(x,n)\ \equiv$ $z:=1$ ; do if $n=0$ then exit fi; do if $\mathsf{o d d}(n)$ then exit fi; comment: This is a comment statement; $n:=n/2$ ; $x:=x*x$ od; $\{n>0\}$ ; $n:=n-1;\ z:=z*x\circ$ d; print $(z)$ .   
end  

Similarly, for listings, use the listings package. \begin{lstlisting} \end{lstlisting} is used to set environments similar to verbatim environment. Refer to the lstlisting package documentation for more details.  

Algorithm 1 Calculate $y=x^{\mathit{n}}$   
Require: $n\geq0\vee x\neq0$   
Ensure: $y=x^{n}$   
1: $y\Leftarrow1$   
2: if $n<0$ then   
3: $\begin{array}{c}{{X\leftarrow1/x}}\\ {{N\leftarrow-n}}\end{array}$   
4:   
5: else   
6: $\begin{array}{c}{{X\leftarrow x}}\\ {{N\leftarrow n}}\end{array}$   
7:   
8: end if   
9: while $N\neq0$ do   
10: if $N$ is even then   
11: $X\Leftarrow X\times X$   
12: $N\Leftarrow N/2$   
13: else[N is odd]   
14: $\begin{array}{c}{{y\Leftarrow y\times X}}\\ {{N\Leftarrow N-1}}\end{array}$   
15:   
16: end if   
17: end while  

f o r i : $\circleddash$ maxint to 0 do   
begin   
{ do nothing }   
end ;   
Write ( ’ Case  i n s e n s i t i v e  ’ ) ; Write ( ’ P a s c a l  keywords . ’ ) ;  

## 8 Cross referencing  

Environments such as figure, table, equation and align can have a label declared via the \label{#label} command. For figures and table environments use the \label{} command inside or just below the \caption{} command. You can then use the \ref{#label} command to cross-reference them. As an example, consider the label declared for Figure 1 which is \label{fig1}. To crossreference it, use the command Figure \ref{fig1}, for which it comes up as “Figure 1”.  

To reference line numbers in an algorithm, consider the label declared for the line number 2 of Algorithm 1 is \label{algln2}. To cross-reference it, use the command \ref{algln2} for which it comes up as line 2 of Algorithm 1.  

### 8.1 Details on reference citations  

Standard LATEX permits only numerical citations. To support both numerical and author-year citations this template uses natbib LATEX package. For style guidance please refer to the template user manual.  

Here is an example for \cite{...}: [1]. Another example for \citep{...}: [2]. For author-year citation mode, \cite{...} prints Jones et al. (1990) and \citep{...} prints (Jones et al., 1990).  

All cited bib entries are printed at the end of this article: [3], [4], [5], [6], [7], [8], [9], [10], [11] and [12].  

## 9 Examples for theorem like environments  

For theorem like environments, we require amsthm package. There are three types of predefined theorem styles exists—thmstyleone, thmstyletwo and thmstylethree  

<html><body><table><tr><td>thmstyleone</td><td>Numbered, theorem head in bold font and theorem text in italic style</td></tr><tr><td>thmstyletwo</td><td>Numbered, theorem head in roman font and theorem text in italic style</td></tr><tr><td>thmstylethree</td><td>Numbered, theorem head in bold font and theorem text in roman style</td></tr></table></body></html>  

For mathematics journals, theorem styles can be included as shown in the following examples:  

Theorem 1 (Theorem subhead) Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text. Example theorem text.  

Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text.  

Proposition 2 Example proposition text. Example proposition text. Example proposition text. Example proposition text. Example proposition text. Example proposition text. Example proposition text. Example proposition text. Example proposition text. Example proposition text.  

Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text.  

Example 1 Phasellus adipiscing semper elit. Proin fermentum massa ac quam. Sed diam turpis, molestie vitae, placerat a, molestie nec, leo. Maecenas lacinia. Nam ipsum ligula, eleifend at, accumsan nec, suscipit a, ipsum. Morbi blandit ligula feugiat magna. Nunc eleifend consequat lorem.  

Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text.  

Remark 1 Phasellus adipiscing semper elit. Proin fermentum massa ac quam. Sed diam turpis, molestie vitae, placerat a, molestie nec, leo. Maecenas lacinia. Nam ipsum ligula, eleifend at, accumsan nec, suscipit a, ipsum. Morbi blandit ligula feugiat magna. Nunc eleifend consequat lorem.  

Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text.  

Definition 1 (Definition sub head) Example definition text. Example definition text. Example definition text. Example definition text. Example definition text. Example definition text. Example definition text. Example definition text.  

Additionally a predefined “proof” environment is available: \begin{proof} \end{proof}. This prints a “Proof” head in italic font style and the “body text” in roman font style with an open square at the end of each proof environment.  

Proof Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. □  

Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text. Sample body text.  

Proof of Theorem 1 Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. Example for proof text. □  

For a quote environment, use \begin{quote}...\end{quote}  

Quoted text example. Aliquam porttitor quam a lacus. Praesent vel arcu ut tortor cursus volutpat. In vitae pede quis diam bibendum placerat. Fusce elementum convallis neque. Sed dolor orci, scelerisque ac, dapibus nec, ultricies ut, mi. Duis nec dui quis leo sagittis commodo.  

Sample body text. Sample body text. Sample body text. Sample body text. Sample body text (refer Figure 1). Sample body text. Sample body text. Sample body text (refer Table 3).  

## 10 Methods  

Topical subheadings are allowed. Authors must ensure that their Methods section includes adequate experimental and characterization data necessary for others in the field to reproduce their work. Authors are encouraged to include RIIDs where appropriate.  

Ethical approval declarations (only required where applicable) Any article reporting experiment/s carried out on (i) live vertebrate (or higher invertebrates), (ii) humans or (iii) human samples must include an unambiguous statement within the methods section that meets the following requirements:  

1. Approval: a statement which confirms that all experimental protocols were approved by a named institutional and/or licensing committee. Please identify the approving body in the methods section   
2. Accordance: a statement explicitly saying that the methods were carried out in accordance with the relevant guidelines and regulations   
3. Informed consent (for experiments involving humans or human tissue samples): include a statement confirming that informed consent was obtained from all participants and/or their legal guardian/s  

If your manuscript includes potentially identifying patient/participant information, or if it describes human transplantation research, or if it reports results of a clinical trial then additional information will be required. Please visit (https://www.nature.com/nature-research/editorial-policies) for Nature Portfolio journals, (https://www.springer.com/gp/authors-editors/ journal-author/journal-author-helpdesk/publishing-ethics/14214) for Springer Nature journals, or (https://www.biomedcentral.com/getpublished/ editorial-policies#ethics+and+consent) for BMC.  

## 11 Discussion  

Discussions should be brief and focused. In some disciplines use of Discussion or ‘Conclusion’ is interchangeable. It is not mandatory to use both. Some journals prefer a section ‘Results and Discussion’ followed by a section ‘Conclusion’. Please refer to Journal-level guidance for any specific requirements.  

## 12 Conclusion  

Conclusions may be used to restate your hypothesis or research question, restate your major findings, explain the relevance and the added value of your work, highlight any limitations of your study, describe future directions for research and recommendations.  

In some disciplines use of Discussion or ’Conclusion’ is interchangeable. It is not mandatory to use both. Please refer to Journal-level guidance for any specific requirements.  
"""
print(markdown_to_tree(md_text))
