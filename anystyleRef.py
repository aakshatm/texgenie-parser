import subprocess
import os
import re

def extract_references(text):
    # Find the last occurrence of "# References" and capture everything after
    match = re.search(r'#\s*references[\s\S]*$', text, re.IGNORECASE)
    
    if match:
        references = re.sub(r'#\s*references\s*\n?', '', match.group(0), flags=re.IGNORECASE)  # Remove "# References"
        
        # Save extracted references to "references.txt"
        with open("references.txt", "w") as f:
            f.write(references)  # Strip extra newlines
        
        # Remove the extracted references from the original text
        original_text = text[:match.start()].rstrip()  # Remove trailing spaces/newlines
        
        return original_text  # Return cleaned text without references
    
    return text  # If no references found, return original text unchanged


def generate_bib(input_file, output_dir="."):
    # mount current directory to docker volume, --rm for remove container after use, anystyle -f bib,json,xml formats supported, --overwrite to overwrite output file if already existing, parse references.txt output_loc

    # docker run --rm -v "$PWD:/data" cokoapps/anystyle:2.0.0     anystyle -f bib --overwrite parse /data/references.txt /data/

    try:
        subprocess.run([
            "docker", "run", "--rm", "-v", f"{os.getcwd()}:/data",
            "cokoapps/anystyle:2.0.0",
            "anystyle", "-f", "bib", "--overwrite", "parse",
            f"/data/{input_file}", "/data/"
        ], check=True)
        
        output_file = os.path.join(output_dir, input_file.replace(".txt", ".bib"))
        print(f"BibTeX file saved as {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Example Usage
text = '''
# TabLeX: A Benchmark Dataset for Structure and Content Information Extraction from Scientific Tables  

Harsh Desai $^{1}$ , Pratik Kayal $^2$ , and Mayank Singh $^{3}$  

1 Indian Institute of Technology, Gandhinagar, India hsd31196@gmail.com   
2 Indian Institute of Technology, Gandhinagar, India pratik.kayal@iitgn.ac.in   
3 Indian Institute of Technology, Gandhinagar, India singh.mayank@iitgn.ac.in  

Abstract. Information Extraction (IE) from the tables present in scientific articles is challenging due to complicated tabular representations and complex embedded text. This paper presents TabLeX, a large-scale benchmark dataset comprising table images generated from scientific articles. TabLeX consists of two subsets, one for table structure extraction and the other for table content extraction. Each table image is accompanied by its corresponding LATEX source code. To facilitate the development of robust table IE tools, TabLeX contains images in different aspect ratios and in a variety of fonts. Our analysis sheds light on the shortcomings of current state-of-the-art table extraction models and shows that they fail on even simple table images. Towards the end, we experiment with a transformer-based existing baseline to report performance scores. In contrast to the static benchmarks, we plan to augment this dataset with more complex and diverse tables at regular intervals.  

# Keywords: Information Extraction · LATEX· Scientific Articles.  

## 1 Introduction  

Tables are compact and convenient means of representing relational information present in diverse documents such as scientific papers, newspapers, invoices, product descriptions, and financial statements [12]. Tables embedded in the scientific articles provide a natural way to present data in a structured manner [5]. They occur in numerous variations, especially visually, such as with or without horizontal and vertical lines, spanning multiple columns or rows, non-standard spacing, alignment, and text formatting [6]. Besides, we also witness diverse semantic structures and presentation formats, dense embedded text, and formatting complexity of the typesetting tools [23]. These complex representations and formatting options lead to numerous challenges in automatic tabular information extraction (hereafter, ‘TIE’ ).  

Table detection vs. extraction: In contrast to table detection task (hereafter, ‘ $T D$ ) that refers to identifying tabular region (e.g., finding a bounding box that encloses the table) in an document, TIE refers to two post identification tasks: (i) table structure recognition (hereafter, ‘TSR’ ) and (ii) table content recognition (hereafter, ‘TCR’ ). TSR refers to the extraction of structural information like rows and columns from the table, and TCR refers to content extraction that is embedded inside the tables. Figure 1 shows an example table image with its corresponding structure and content information in the TEX language. Note that, in this paper, we only focus on the two TIE tasks.  

Limitations in existing state-of-the-art TIE systems: There are several state-of-the-art tools (Camelot $^4$ ,Tabula $^5$ , PDFPlumber $^6$ , and Adobe Acrobat SDK $^7$ ) for text-based TIE. On the contrary, Tesseract-based OCR [24] is commercially available tool which can be used for image-based TIE. However, these tools perform poorly on the tables embedded in the scientific papers due to the complexity of tables in terms of spanning cells and presence of mathematical content. The recent advancements in deep learning architectures (Graph Neural Networks [32] and Transformers [28]) have played a pivotal role in developing the majority of the image-based TIE tools. We attribute the limitations in the current image-based TIE primarily due to the training datasets’ insufficiency. Some of the critical issues with the training datasets can be (i) the size, (ii) diversity in the fonts, (iii) image resolution (in dpi), (iv) aspect ratios, and (v) image quality parameters (blur and contrast).  

Our proposed benchmark dataset: In this paper, we introduce TabLeX, a benchmark dataset for information extraction from tables embedded inside scientific documents compiled using LATEX-based typesetting tools. TabLeX is composed of two subsets—a table structure subset and a table content subset—to extract the structure and content information. The table structure subset contains more than three million images, whereas the table content subset contains over one million images. Each tabular image accompanies its corresponding ground-truth program in TEX macro language. In contrast to the existing datasets [3,30,31], TabLeX comprises images with 12 different fonts and multiple aspect ratios.  

Main contributions: The main contributions of the paper are:  

1. Robust preprocessing pipeline to process the scientific documents (created in TEX language) and extract the tabular spans.   
2. A large-scale benchmark dataset, TabLeX, comprising more than three million images for structure recognition task and over one million images for the content recognition task.   
3. Inclusion of twelve font types and multiple aspect ratios during the dataset generation process.   
4. Evaluation of state-of-the-art computer vision based baseline [7] on TabLeX.  

The paper outline : We organize the paper into several sections. Section 2 reviews existing datasets and corresponding extraction methodologies. Section 3 describes the preprocessing pipeline and presents TabLeX dataset statistics. Section 4 details three evaluation metrics. Section 5 presents the the baseline and discusses the experimental results and insights. Finally, we conclude and identify the future scope in Section 6.  

<html><body><table><tr><td>Nuclide</td><td>NPADimension</td><td>FCIDimension</td></tr><tr><td>52Fe</td><td>350</td><td>1.1×108</td></tr><tr><td>53Fe</td><td>6106</td><td>2.2×108</td></tr><tr><td>54Fe</td><td>706</td><td>3.5×108</td></tr><tr><td>56Fe</td><td>1276</td><td>5.0x 108</td></tr><tr><td colspan="3">(a) Table Image {ccc}\hlineCELL&CELL&CELL\ hlineCELL&CELL&CELL\\hlineCELL& CELL&CELLhlineCELL&CELL&CELL \hlineCELL&CELL&CELL\hline (b) Structure Information NuclideI&NPAIDimensionI&FCilDimension \${52$Fe&350&$1.1\tmes108 $53$Fe&6106&$2.2\times10811$</td></tr></table></body></html>  

Fig. 1: Example of table image along with its structure and content information from the dataset. Tokens in content information are character-based, and the ‘¦’ token acts as a delimiter to identify words out of a continuous stream of characters.  

## 2 The Current State Of The Research  

In recent years, we witness a surge in the digital documents available online due to the high availability of communication facilities and large-scale internet infrastructure. In particular, the availability of scientific research papers that contain complex tabular structures has grown exponentially. However, we witness fewer research efforts to extract embedded tabular information automatically. Table 1 lists some of the popular datasets for TD and TIE tasks. Among the two tasks, there are very few datasets available for the TIE, specifically from scientific domains containing complex mathematical formulas and symbols. As the current paper primarily focuses on the TIE from scientific tables, we discuss some of the popular datasets and their limitations in this domain.  

Scientific tabular datasets: Table2Latex [3] dataset contains 450k scientific table images and its corresponding ground-truth in LATEX. It is curated from  

Table 1: Datasets and methods used for Table Detection (TD), Table Structure Recognition (TSR) and Table Recognition (TR). \* represents scientific paper datasets.  

<html><body><table><tr><td colspan="2">Datasets</td><td>TD</td><td>TSR</td><td></td><td>TRFormat</td><td># Tables</td><td>Methods</td></tr><tr><td colspan="2">Marmot[26]*</td><td></td><td>×</td><td></td><td>PDF</td><td>958</td><td>Pdf2Table[21],TableSeer[15],[10]</td></tr><tr><td colspan="2">PubLayNet[31]*</td><td></td><td>×</td><td></td><td>PDF</td><td>113k</td><td>F-RCNN[19], M-RCNN[11]</td></tr><tr><td colspan="2">DeepFigures[22]</td><td>√</td><td></td><td></td><td>PDF</td><td>1.4m</td><td>Deepfigures[22]</td></tr><tr><td colspan="2">ICDAR2013[9]</td><td>人</td><td>人</td><td></td><td>PDF</td><td>156</td><td>Heuristics+ML</td></tr><tr><td colspan="2">ICDAR2019[8]</td><td>人</td><td>人</td><td></td><td>Images</td><td>3.6k</td><td>Heuristics+ML</td></tr><tr><td colspan="2">UNLV[20]</td><td>√</td><td>人</td><td></td><td>Images</td><td>558</td><td>T-Recs[13]</td></tr><tr><td colspan="2">TableBank[14]*</td><td>√</td><td></td><td></td><td>Images</td><td>417k (TD)</td><td>F-RCNN[19]</td></tr><tr><td colspan="2">TableBank[14]*</td><td>√</td><td></td><td>X</td><td>Images</td><td>145k (TSR)</td><td>WYGIWYS[2]</td></tr><tr><td colspan="2">SciTSR[1]*</td><td></td><td></td><td>√</td><td>PDF</td><td>15k</td><td>GraphTSR[1]</td></tr><tr><td colspan="2">Table2Latex[3]*</td><td></td><td></td><td>√</td><td>Images</td><td>450k</td><td>IM2Tex[4]</td></tr><tr><td colspan="2">Synthetic data[18</td><td>X</td><td>人</td><td>√</td><td>Images</td><td>Unbounded</td><td>DCGNN[18]</td></tr><tr><td colspan="2">PubTabNet[30]*</td><td></td><td></td><td>√</td><td>Images</td><td>568k</td><td>EDD[30]</td></tr><tr><td colspan="2">TABLEX (ours)*</td><td></td><td></td><td>√</td><td>Images</td><td>1m+</td><td>TRT [7]</td></tr></table></body></html>  

the $a r X i v^{8}$ repository. To the best of our knowledge, Table2Latex is the only dataset that contains ground truth in TEX language but is not publicly available. TableBank [14] contains 145k table images along with its corresponding ground truth in the HTML representation. TableBank [14] contains table images from both Word and LATEX documents curated from the internet and $a r X i v^{8}$ , respectively. However, it does not contain content information to perform the TCR task. PubTabNet [30] contains over 568k table images and corresponding ground truth in the HTML language. PubTabNet is curated from the PubMed Central repository9. However, it is only limited to the biomedical and life sciences domain. SciTSR [1] contains 15k tables in the PDF format with table cell content and the coordinate information in the JSON format. SciTSR has been curated from the arXiv $^{8}$ repository. However, manual analysis tells that 62 examples out of 1000 randomly sampled examples are incorrect [29].  

TIE methodologies: The majority of the TIE methods employ encoder-decoder architecture [3,14,30]. Table2Latex [3] uses IM2Tex [4] model where encoder consists of convolutional neural network (CNN) followed by bidirectional LSTM and decoder consists of standard LSTM. TableBank [14] uses WYGIWS [2] model, an encoder-decoder architecture, where encoder consists of CNN followed by a recurrent neural network (RNN) and decoder consists of standard RNN. PubTabNet [30] uses a proposed encoder-dual-decoder (EDD) [30] model which consists of CNN encoder and two RNN decoders called structure and cell decoder, respectively. In contrast to the above works, SciTSR [1] proposed a graph neural network-based extraction methodology. The network takes vertex and edge features as input and computes their representations using graph attention blocks, and performs classification over these edges.  

TIE metrics: Table2Latex [3] used BLEU [16] score (a text-based metric) and exact match accuracy (a vision-based metric) for evaluation. TableBank [14] also conducted BLEU [16] metric for evaluation. Tesseract OCR [25] uses the Word Error Rate (WER) metric for evaluation of the output. SciTSR [1] uses microand macro-averaged precision, recall, and F1-score to compare the output against the ground truth, respectively. In contrast to the above standard evaluation metrics in NLP literature, PubTabNet [30] proposed a new metric called TreeEdit-Distance-based Similarity (TEDS) for evaluation of the output HTML representation.  

The challenges: Table 1 shows that there are only two datasets for Image-based TCR from scientific tables, that is, Table2Latex [3] and PubTabNet [30]. We address some of the challenges from previous works with TabLeX which includes (i) large-size for training (ii) Font-agnostic learning (iii) Image-based scientific TCR (iv) domain independent  

## 3 The TabLeX Dataset  

This section presents the detailed curation pipeline to create the TabLeX dataset.   
Next, we discuss the data acquisition strategy.  

### 3.1 Data Acquisition  

We curate data from popular preprint repository arXiv 8. We downloaded paper (uploaded between Jan 2019–Sept 2020) source code and corresponding compiled PDF. These articles belong to eight subject categories. Figure 2 illustrates category-wise paper distribution. As illustrated, the majority of the papers belong to three subject categories, physics $(33.93\%$ ), computer science $(25.79\%)$ ), and mathematics (23.27%). Overall, we downloaded 347,502 papers and processed them using the proposed data processing pipeline (described in the next section).  

### 3.2 Data Processing Pipeline  

The following steps present a detailed description of the data processing pipeline.  

# LATEX Code Pre-Processing Steps  

1. Table Snippets Extraction: A table snippet is a part of LATEX code that begins with ‘\begin{tabular}’ and ends with ‘\end{tabular}’ command. During its extraction, we removed citation command ‘\cite{}’, reference command ‘\ref{}’, label command ‘\label{}’, and graphics command ‘\includegraphics[]{}’, along with $\sim$ symbol (preceding these commands). Also, we remove command pairs (along with the content between them) like ‘\begin{figure}’ and ‘\end{figure}’, and ‘\begin{subfigure}’ and ‘\end{subfigure}’, as they cannot be predicted from the tabular images.  

![](images/ac85b1d7575a99d441ea5b1d37a2ca2d63b0453e5f9fb9570c5227dadd2daf14.jpg)  
Fig. 2: Total number of papers in arXiv’s subject categories. Here SS denotes Systems Science.  

Furthermore, we also remove the nested table environments. Figure 3a and 3b show an example table and its corresponding LATEX source code, respectively.  

2. Comments Removal: Comments are removed by removing the characters between ‘%’ token and newline token ‘\n’. This step was performed because comments do not contribute to visual information.  

3. Column Alignment and Rows Identification: We keep all possible alignment tokens (‘l’, ‘r’, and ‘ $\mathtt{c^{\prime}}$ ) specified for column styling. The token ‘|’ is also kept to identify vertical lines between the columns, if present. The rows are identified by keeping the ‘\\’ and ‘\tabularnewline’ tokens. These tokens signify the end of each row in the table. For example, Figure 3c shows extracted table snippet from LATEX source code (see Figure 3b) containing the column and rows tokens with comment statements removed.  

4. Font Variation: In this step, the extracted LATEX code is augmented with different font styles. We experiment with a total 12 different LATEX font packages10. We use popular font packages from PostScript family which includes ‘courier’, ‘helvet’, ‘palatino’, ‘bookman’, ‘mathptmx’, ‘utopia’ and also other font packages such as ‘tgbonum’, ‘tgtermes’, ‘tgpagella’, ‘tgschola’, ‘charter and ‘tgcursor’. For each curated image, we create 12 variations, one in each of the font style.  

5. Image Rendering: Each table variant is compiled into a PDF using a LATEX code template (described in Figure 3d). Here, ‘table snippet’ represents the extracted tabular LATEX code and ‘font package’ represents the LATEX font package used to generated the PDF. The corresponding table PDF files are then converted into JPG images using the Wand library $_{11}$ which uses ImageMagick [27] API to convert PDF into images. Figure 3e shows the  

8 Please add the following required packages to your document   
\begin{table} [t!] \small \centering \begin{tabular}{1cc} \hline \multicolumn{1}{l}{\textbf{Technique}} & \multicolumn{1}{c}{\textbf{\approach{}}} \multicolumn{1}{c}{\textbf{\approach{} (BERT)}} II hline \hline Base mode1 & 40.5\8 & 53.9\8 11 8 \hspace{2mm]+EL & 47.1\8 & 60.3\8 11 \hspace[2mm}+SL & 48.5\8 & 60.3\8 11 \hspace{2mm}+SL + MEM & 51.3\8 & 60.6\8 1\ \hspace2mm+SL+MEM + CF &53.2\& 61.9\8 \ \hline \end{tabular} \caption{\label{tab:ablation results} Ablation study   
results. Base model means that we does not perform schema   
linking (SL), memory augmented pointer network (Mem) and the   
coarse-to-fine framework (cr) on it.} Itahlel  

<html><body><table><tr><td colspan="2">Technique</td><td>(BERT)</td></tr><tr><td>Basemodel</td><td>40.5%</td><td>53.9%</td></tr><tr><td>+SL</td><td>48.5%</td><td>60.3%</td></tr><tr><td>+SL+MEM</td><td>51.3%</td><td>60.6%</td></tr><tr><td>+SL+MEM+CF</td><td>53.2%</td><td>61.9%</td></tr></table></body></html>  

# (b) Corresponding LATEX source code  

\begin{tabular}{lcc} \hline \multicolumn{1}{1}{\textbf{Technique}} & \multicolumn{1}{c}{\textbf{\approach{}}}& \multicolumn{1}{c}{\textbf{\approach{} (BERT)}}\ \hline \hline Base model & 40.5\8 & 53.9\8 1\ \hspace{2mm}+SL & 48.5\8 & 60.3\8 11 \hspace{2mm}+SL + MEM & 51.3\8 & 60.6\8 \\ \hspace{2mm}+SL+MEM + CF &53.2\8 & 61.9\8 \\ \hline   
\end{tabular}  

![](images/d01386590ad36577a2363d9b0bb03e7e2c76c15ab1791726c05019e8e2a791c2.jpg)  
(a) A real table image   
(d) $\mathrm{{\mathbb{A}T}E X}$ code template  

<html><body><table><tr><td>Technique</td><td></td><td>(BERT)</td></tr><tr><td>Basemodel</td><td>40.5%</td><td>53.9%</td></tr><tr><td>+SL</td><td>48.5%</td><td>60.3%</td></tr><tr><td>+SL+MEM</td><td>51.3%</td><td>60.6%</td></tr><tr><td>+SL+ MEM + CF</td><td>53.2%</td><td>61.9%</td></tr></table></body></html>  

(e) Code with Charter font package (f) The final generated table image  

embedded code and font information within the template. Figure 3f shows the final table image with Charter font. During conversion, we kept the image’s resolution as 300 dpi, set the background color of the image to white, and removed the transparency of the alpha channel by replacing it with the background color of the image. We use two types of aspect ratio variations during the conversion, described as follows:  

(a) Conserved Aspect Ratio: In this case, the bigger dimension (height or width) of the image is resized to 400 pixels12. We then resize the smaller dimension (width or height) by keeping the original aspect ratio conserved. During resizing, we use a blur factor of 0.8 to keep images sharp.   
(b) Fixed Aspect Ratio: The images are resized to a fixed size of 400 $\times$ 400 pixels using a blur factor of 0.8. Note that this resizing scheme can lead to extreme levels of image distortions.  

### LATEX Code Post-Processing Steps for Ground-Truth Preparation  

1. Filtering Noisy LATEX tokens: We filter out LATEX environment tokens (tokens starting with ‘\’) having very less frequency (less than 5000) in the overall corpus compared to other LATEX environment tokens and replaced it with ‘\LATEX_TOKEN’ as these tokens will have a little contribution. This frequency-based filtering reduced the corpus’s overall vocabulary size, which helps in training models on computation or memory-constrained environments.  

2. Structure Identification: In this post-processing step, we create Table Structure Dataset (TSD). It consists of structural information corresponding to the table images. We keep tabular environment parameters as part of structure information and replace tokens representing table cells’ content with a placeholder token ‘CELL’. This post-processing step creates ground truth for table images in TSD. Specifically, the vocabulary comprises digits (0- 9), ‘&’, ‘CELL’, ‘\\’, ‘\hline’, ‘\multicolumn’, ‘\multirow’, ‘\bottomrule’, ‘\midrule’, ‘\toprule’, ‘|’, ‘l’, ‘r’, ‘c’, ‘ ’, and ‘ ’. A sample of structure information is shown in Figure 1b, where the ‘CELL’ token represents a cell structure in the table. Structural information can be used to identify the number of cells, rows, and columns in the table using ‘CELL’, ‘\\’ and alignment tokens (‘c’, ‘l’, and ‘r’), respectively. Based on output sequence length, we divided this dataset further into two variants TSD-250 and TSD500, where the maximum length of the output sequence is 250 and 500 tokens, respectively.  

3. Content Identification: Similar to TSD, we also create a Table Content Dataset (TCD). This dataset consists of content information including alphanumeric characters, mathematical symbols, and other LATEX environment tokens. Content tokens are identified by removing tabular environment parameters and keeping only the tokens that identify table content. Specifically, the vocabulary includes all the alphabets (a-z and A-Z), digits (0-9), LATEX environment tokens (‘\textbf’, \hspace’, etc.), brackets $(^{\cdot}(^{\cdot},{}^{\cdot})^{\cdot},{}^{\cdot}\{^{\cdot},{}^{\cdot}\}^{\cdot}$ ’, etc.)  

Table 2: TabLeX Statistics. ML denotes the maximum length of output sequence. Samples denotes the total number of table images. T/S denotes the average number of tokens per sample. VS denotes the vocabulary size. AR and AC denote the average number of rows and columns among all the samples in the four dataset variants, respectively.  

<html><body><table><tr><td>Dataset</td><td>ML</td><td>Samples</td><td colspan="3">Train/Val/Test</td><td>T/S</td><td>VS</td><td>AR</td><td>AC</td></tr><tr><td>TSD-250</td><td>250</td><td>2,938,392</td><td>2,350,713</td><td>293,839</td><td>293,840</td><td>74.09</td><td>25</td><td>6</td><td>4</td></tr><tr><td>TSD-500</td><td>500</td><td>3,191,891</td><td>2,553,512 /</td><td>319,189 319,190</td><td>95.39</td><td>25</td><td></td><td>8</td><td>5</td></tr><tr><td>TCD-250</td><td>250</td><td>1,105,636</td><td>884,508</td><td>110,564 110,564</td><td></td><td>131.96</td><td>718</td><td>4</td><td>4</td></tr><tr><td>TCD-500</td><td>500</td><td>1,937,686</td><td></td><td>1,550,148/193,769/193,769</td><td></td><td>229.06</td><td>737</td><td>5</td><td>4</td></tr></table></body></html>  

and all other possible symbols ( $\mathfrak{P}$ ’, ‘&’, etc.). In this dataset, based on output sequence length, we divided it further into two variants TCD-250 and TCD-500, where the maximum length of the output sequence is 250 and 500 tokens, respectively. A sample of content information is shown in Figure 1c.  

### 3.3 Dataset Statistics  

We further partition each of the four dataset variants TSD-250, TSD-500, TCD25, and TCD-500, into training, validation, and test sets in a ratio of 80:10:10. Table 2 shows the summary of the dataset. Note that the number of samples present in the TSD and the corresponding TCD can differ due to variation in the output sequence’s length. Also, the average number of tokens per sample in TCD is significantly higher than the TSD due to more information in the tables’ content than the corresponding structure. Figure 4 demonstrates histograms representing the token distribution for the TSD and TCD. In the case of TSD, the majority of tables contain less than 25 tokens. Overall the token distribution shows a longtail behavior. In the case of TCD, we witness a significant proportion between 100–250 tokens. The dataset is licensed under Creative Commons Attribution 4.0 International License and available for download at https://www.tinyurl.com/ tablatex.  

## 4 Evaluation Metrics  

We experiment with three evaluation metrics to compare the predicted sequence of tokens $\overset{\prime}{T}_{P T}\mathrm{~,~}$ ) against the sequence of tokens in the ground truth $(T_{G T})$ . Even though the proposed metrics are heavily used in NLP research, few TIE works have leveraged them in the past. Next, we discuss these metrics and illustrate the implementation details using a toy example described in Figure 5.  

1. Exact Match Accuracy (EMA): EMA outputs the fraction of predictions with exact string match of $T_{P T}$ against $T_{G T}$ . A model having a higher value of EMA is considered a good model. In Figure 5, for the TSR task, $T_{P T}$ misses ‘\hline’ token compared to the corresponding $T_{G T}$ , resulting in EMA $=0$ . Similarly, the $T_{P T}$ exactly matches the $T_{G T}$ for the TCR task, resulting in $\mathrm{EMA}=1$ .  

![](images/2e6e975c131d5ec481d46314a55c4e55177a6130cc9d2a78903450791a3aae01.jpg)  
Fig. 4: Histograms representing the number of tokens distribution for the tables present in the dataset.  

2. Bilingual Evaluation Understudy Score (BLEU): The BLEU [16] score is primarily used in Machine Translation literature to compare the quality of the translated sentence against the expected translation. Recently, several TIE works [2,4] have adapted BLEU for evaluation. It counts the matching ngrams in $T_{P T}$ against the n-grams in $T_{G T}$ . The comparison is made regardless of word order. The higher the BLEU score, the better is the model. We use SacreBLEU [17] implementation for calculating the BLEU score. We report scores for the most popular variant, BLEU-4. BLEU-4 refers to the product of brevity penalty (BP) and a harmonic mean of precisions for unigrams, bigrams, 3-grams, and 4-grams (for more details see [16]). Figure 5, there is an exact match between $T_{P T}$ and $T_{G T}$ for TCR task yielding BLEU = 100.00. In the case of TSR, the missing ‘\hline’ token in $T_{P T}$ yields a lower BLEU = 89.66.  

3. Word Error Rate (WER): WER is defined as a ratio of the Levenshtein distance between the $T_{P T}$ and $T_{G T}$ to the length of $T_{G T}$ . It is a standard evaluation metric for several OCR tasks. Since it measures the rate of error, models with lower WER are better. We use jiwer $^{.13}$ Python library for WER computation. In Figure 5, for the TCR task, the WER between $T_{P T}$ and $T_{G T}$ is 0. Whereas in the case of TSR, the Levenshtein distance between $T_{P T}$ and $T_{G T}$ is one due to the missing ‘\hline’ token. Since the length of $T_{G T}$ is 35, WER comes out to be 0.02.  

![](images/5a7dc443a66f7e2939dd785707afb7902cf244ff97357639e8da1f965097f0a9.jpg)  
Fig. 5: (a) A toy table, (b) corresponding ground truth token sequence for TSR and TCR tasks, (c) model output sequence for TCR task, and (d) model output sequence for TSR task.  

## 5 Experiments  

In this section, we experiment with a deep learning-based model for TSR and TCR tasks. We adapt an existing model [7] architecture proposed for the scene text recognition task and train it from scratch on the TabLeX dataset. It uses partial ResNet-101 along with a fully connected layer as a feature extractor module for generating feature embeddings with a cascaded Transformer [28] module for encoding the features and generating the output. Figure 6 describes the detailed architecture of the model. Note that in contrast to the scene image as an input in [7], we input a tabular image and predict the LATEX token sequence. We term it as the TIE-ResNet-Transformer model (TRT ).  

### 5.1 Implementation Details  

For both TSR and TCR tasks, we train a similar model. We use the third intermediate hidden layer of partial ResNet-101 and an FC layer as a feature extractor module to generate a feature map. The generated feature map (size = $625\times1024$ ) is further embedded into 256 dimensions, resulting in reduced size of $625\times256$ . We experiment with four encoders and eight decoders with learnable positional embeddings. The models are trained for ten epochs with a batch size of 32 using cross-entropy loss function and Adam Optimizer with an initial learning rate of 0.1 and 2000 warmup training steps, decreasing with Noam’s learning rate decay scheme. A dropout rate of 0.1 and $\epsilon_{l s}=0.1$ label smoothing parameter is used for regularization. For decoding, we use the greedy decoding technique in which the model generates an output sequence of tokens in an auto-regressive manner, consuming the previously generated tokens to generate the next token. All the experiments were performed on 4 $\times$ NVIDIA V100 graphics card.  

![](images/4ea4a5555ce29b5f703786d8de729815ca3fad411d31aa20df7608e7e29dae78.jpg)  
Fig. 6: TIE-ResNet-Tr ansformer model architecture.  

### 5.2 Results  

Table 3 illustrates that higher sequence length significantly degrades the EMA score for both the TSR and TCR tasks. For TCD-250 and TCD-500, high BLEU scores ( $>$ 90) suggest that the model can predict a large chunk of LATEX content information correctly. However, the errors are higher for images with a conserved aspect ratio than with a fixed aspect ratio, which is confirmed by comparing their BLEU score and WER metrics. Similarly, for TSD-250 and TSD-500, high EMA and lower WER suggest that the model can correctly identify structure information for most of the tables. TCD yields a lower EMA score than TSD. We attribute this to several reasons. One of the reasons is that the TCR model fails to predict some of the curly braces (‘{’ and ‘}’) and dollar ( $\cdot\mathbb{S}$ ’) tokens in the predictions. After removing curly braces and dollar tokens from the ground truth and predictions, EMA scores for conserved and fixed aspect ratio images in TCD-250 increased to 68.78% and $75.33\%$ , respectively. Similarly, for TCD-500, EMA for conserved and fixed aspect ratio images increases to $49.23\%$ and $59.94\%$ , respectively. In contrast, TSD do not contain dollar tokens, and curly braces are only present at the beginning of the column labels, leading to higher EMA scores. In the future, we believe the results can be improved significantly by proposing better vision-based DL architectures for TSR and TCR tasks.  

<html><body><table><tr><td colspan="5">Table3:TRTresults ontheTABLEXdataset.</td></tr><tr><td>TCD</td><td>DatasetAspectRatio</td><td>EMA(%)</td><td>BLEU</td><td>WER(%)</td></tr><tr><td rowspan="2">250</td><td>Conserved</td><td>21.19</td><td>95.18</td><td>15.56</td></tr><tr><td>Fixed</td><td>20.46</td><td>96.75</td><td>14.05</td></tr><tr><td rowspan="2">TCD 500</td><td>Conserved</td><td>11.01</td><td>91.13</td><td>13.78</td></tr><tr><td>Fixed</td><td>11.23</td><td>94.34</td><td>11.12</td></tr><tr><td rowspan="2">TSD 250</td><td>Conserved</td><td>70.54</td><td>74.75</td><td>3.81</td></tr><tr><td>Fixed</td><td>74.02</td><td>70.59</td><td>4.98</td></tr><tr><td rowspan="2">TSD 500</td><td>Conserved</td><td>70.91</td><td>82.72</td><td>2.78</td></tr><tr><td>Fixed</td><td>71.16</td><td>61.84</td><td>9.34</td></tr></table></body></html>  

## 6 Conclusion  

This paper presents a benchmark dataset TabLeX for structure and content information extraction from scientific tables. It contains tabular images in 12 different fonts with varied visual complexities. We also proposed a novel preprocessing pipeline for dataset generation. We evaluate the existing state-of-the-art transformer-based model and show excellent future opportunities in developing algorithms for IE from scientific tables. In the future, we plan to continuously augment the dataset size and add more complex tabular structures for training and prediction.  

## Acknowledgment  

This work was supported by The Science and Engineering Research Board (SERB), under sanction number ECR/2018/000087.  

## References  

1. Chi, Z., Huang, H., Xu, H., Yu, H., Yin, W., Mao, X.: Complicated table structure recognition. CoRR abs/1908.04729 (2019), http://arxiv.org/abs/1908.04729   
2. Deng, Y., Kanervisto, A., Rush, A.M.: What you get is what you see: A visual markup decompiler. ArXiv abs/1609.04938 (2016)   
3. Deng, Y., Rosenberg, D., Mann, G.: Challenges in end-to-end neural scientific table recognition. In: 2019 International Conference on Document Analysis and Recognition (ICDAR). pp. 894–901 (2019). https://doi.org/10.1109/ICDAR.2019.00148   
4. Deng, Y., Kanervisto, A., Ling, J., Rush, A.M.: Image-to-markup generation with coarse-to-fine attention. In: Proceedings of the 34th International Conference on Machine Learning - Volume 70. p. 980–989. ICML’17, JMLR.org (2017)   
5. Douglas, S., Hurst, M., Quinn, D., et al.: Using natural language processing for identifying and interpreting tables in plain text. In: Proceedings of the Fourth Annual Symposium on Document Analysis and Information Retrieval. pp. 535–546 (1995)   
6. Embley, D.W., Hurst, M., Lopresti, D.P., Nagy, G.: Table-processing paradigms: a research survey. Int. J. Document Anal. Recognit. 8(2-3), 66– 86 (2006). https://doi.org/10.1007/s10032-006-0017-x, https://doi.org/10.1007/ s10032-006-0017- $_\mathrm{x}$   
7. Feng, X., Yao, H., Yi, Y., Zhang, J., Zhang, S.: Scene text recognition via transformer. arXiv preprint arXiv:2003.08077 (2020)   
8. Gao, L., Huang, Y., Dejean, H., Meunier, J., Yan, Q., Fang, Y., Kleber, F., Lang. E.: Icdar 2019 competition on table detection and recognition (ctdar). In: 2019 International Conference on Document Analysis and Recognition (ICDAR). pp. 1510–1515 (2019). https://doi.org/10.1109/ICDAR.2019.00243   
9. Gobel, M., Hassan, T., Oro, E., Orsi, G.: Icdar 2013 table competition. In: 2013 12th International Conference on Document Analysis and Recognition. pp. 1449–1453 (2013). https://doi.org/10.1109/ICDAR.2013.292   
10. Hao, L., Gao, L., Yi, X., Tang, Z.: A table detection method for pdf documents based on convolutional neural networks. DAS pp. 287–292 (2016)   
11. He, K., Gkioxari, G., Dollar, P., Girshick, R.B.: Mask R-CNN. CoRR abs/1703.06870 (2017), http://arxiv.org/abs/1703.06870   
12. Kasar, T., Bhowmik, T.K., Belaid, A.: Table information extraction and struc. ture recognition using query patterns. In: 2015 13th International Conference on Document Analysis and Recognition (ICDAR). pp. 1086–1090 (2015). https://doi.org/10.1109/ICDAR.2015.7333928   
13. Kieninger, T., Dengel, A.: A paper-to-html table converting system. In: Proceedings of document analysis systems (DAS). vol. 98, pp. 356–365 (1998)   
14. Li, M., Cui, L., Huang, S., Wei, F., Zhou, M., Li, Z.: Tablebank: Table benchmark for image-based table detection and recognition. CoRR abs/1903.01949 (2019), http://arxiv.org/abs/1903.01949   
15. Liu, Y., Bai, K., Mitra, P., Giles, C.L.: Tableseer: Automatic table metadata extraction and searching in digital libraries. In: Proceedings of the 7th ACM/IEEE-CS Joint Conference on Digital Libraries. p. 91–100. JCDL ’07, Association for Computing Machinery, New York, NY, USA (2007). https://doi.org/10.1145/1255175.1255193, https://doi.org/10.1145/1255175. 1255193   
16. Papineni, K., Roukos, S., Ward, T., Zhu, W.J.: Bleu: a method for automatic evaluation of machine translation. In: Proceedings of the 40th Annual Meeting of the Association for Computational Linguistics. pp. 311–318. Association for Computational Linguistics, Philadelphia, Pennsylvania, USA (Jul 2002). https://doi.org/10.3115/1073083.1073135, https://www.aclweb.org/ anthology/P02-1040   
17. Post, M.: A call for clarity in reporting BLEU scores. In: Proceedings of the Third Conference on Machine Translation: Research Papers. pp. 186–191. Association for Computational Linguistics, Belgium, Brussels (Oct 2018), https://www.aclweb.org/ anthology/W18-6319   
18. Qasim, S.R., Mahmood, H., Shafait, F.: Rethinking table parsing using graph neural networks. CoRR abs/1905.13391 (2019), http://arxiv.org/abs/1905.13391   
19. Ren, S., He, K., Girshick, R., Sun, J.: Faster r-cnn: Towards real-time object detection with region proposal networks. In: Cortes, C., Lawrence, N., Lee, D., Sugiyama, M., Garnett, R. (eds.) Advances in Neural Information Processing Systems. vol. 28, pp. 91–99. Curran Associates, Inc. (2015), https://proceedings. neurips.cc/paper/2015/file/14bfa6bb14875e45bba028a21ed38046-Paper.pdf   
20. Shahab, A., Shafait, F., Kieninger, T., Dengel, A.: An open approach towards the benchmarking of table structure recognition systems. In: Proceedings of the 9th IAPR International Workshop on Document Analysis Systems. p. 113–120. DAS ’10, Association for Computing Machinery, New York, NY, USA (2010). https://doi.org/10.1145/1815330.1815345, https://doi.org/10.1145/1815330. 1815345   
21. Shigarov, A., Mikhailov, A., Altaev, A.: Configurable table structure recognition in untagged pdf documents. In: Proceedings of the 2016 ACM Symposium on Document Engineering. p. 119–122. DocEng ’16, Association for Computing Machinery, New York, NY, USA (2016). https://doi.org/10.1145/2960811.2967152, https://doi.org/ 10.1145/2960811.2967152   
22. Siegel, N., Lourie, N., Power, R., Ammar, W.: Extracting scientific figures with distantly supervised neural networks. In: Proceedings of the 18th ACM/IEEE on Joint Conference on Digital Libraries. p. 223–232. JCDL ’18, Association for Computing Machinery, New York, NY, USA (2018). https://doi.org/10.1145/3197026.3197040, https://doi.org/10.1145/3197026.3197040   
23. Singh, M., Sarkar, R., Vyas, A., Goyal, P., Mukherjee, A., Chakrabarti, S.: Automated early leaderboard generation from comparative tables. In: European Conference on Information Retrieval. pp. 244–257. Springer (2019)   
24. Smith, R.: An overview of the tesseract ocr engine. In: Proc. Ninth Int. Conference on Document Analysis and Recognition (ICDAR). pp. 629–633 (2007)   
25. Smith, R.: An overview of the tesseract ocr engine. In: Ninth International Conference on Document Analysis and Recognition (ICDAR 2007). vol. 2, pp. 629–633. IEEE (2007)   
26. Tao, X., Liu, Y., Fang, J., Qiu, R., Tang, Z.: Dataset, ground-truth and performance metrics for table detection evaluation. In: Document Analysis Systems, IAPR International Workshop on. pp. 445–449. IEEE Computer Society, Los Alamitos, CA, USA (mar 2012). https://doi.org/10.1109/DAS.2012.29, https://doi.ieeecomputersociety.org/10.1109/DAS.2012.29   
27. The ImageMagick Development Team: Imagemagick, https://imagemagick.org   
28. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, L., Polosukhin, I.: Attention is all you need. In: Advances in neural information processing systems. pp. 5998–6008 (2017)   
29. Wu, G., Zhou, J., Xiong, Y., Zhou, C., Li, C.: Tablerobot: an automatic annotation method for heterogeneous tables. Personal and Ubiquitous Computing pp. 1–7 (2021)   
30. Zhong, X., ShafieiBavani, E., Jimeno Yepes, A.: Image-based table recognition: Data, model, and evaluation. In: Vedaldi, A., Bischof, H., Brox, T., Frahm, J.M. (eds.) Computer Vision – ECCV 2020. pp. 564–580. Springer International Publishing, Cham (2020)   
31. Zhong, X., Tang, J., Jimeno-Yepes, A.: Publaynet: largest dataset ever for document layout analysis. CoRR abs/1908.07836 (2019), http://arxiv.org/abs/1908.07836   
32. Zhou, J., Cui, G., Zhang, Z., Yang, C., Liu, Z., Sun, M.: Graph neural networks: A review of methods and applications. CoRR abs/1812.08434 (2018), http://arxiv. org/abs/1812.08434  
'''

cleaned_text = extract_references(text)

# cleaned_text is text without references
print(cleaned_text)

generate_bib("references.txt")