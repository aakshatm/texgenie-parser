#include <iostream> 
using namespace std;

enum ElementType{
    HEADING, IMG, TEXT, TABLE, LIST, LINK, CODE, BLOCKQUOTE, HR, HTML, SECTION
};

class Element{
    public: 
    int order; 
    ElementType type;
    std::string content;
    std::vector<Element> children;
    Element(ElementType t, std::string c) : type(t), content(c) {}
    Element(ElementType t) : type(t) {}
    void addChild(Element child) {
        children.push_back(child);
    }
    void addChild(ElementType t, std::string c) {
        children.push_back(Element(t, c));
    }
    void addChild(ElementType t) {
        children.push_back(Element(t));
    }
    void print() {
        cout << "Element " << content << endl; 
        for (auto child: children){
            child.print();
        }
    }
};

class Heading : public Element { 
    public: 
    void print() {
        cout << "Heading " << content << endl; 
        for (auto child: children){
            child.print();
        }
    }
};

class Text : public Element { 
    public: 
    void print() {
        cout << "Text " << content << endl; 
        for (auto child: children){
            child.print();
        }
    }
}; 

class Parser {
    public: 
    vector<Element> elements; 
    string markDownText; 


    void convertMarkDownToElements(string text) {
        markDownText = text; 
        // Parse the markdown text and create elements
        // For simplicity, we will just create a single element
        Element e(HEADING, "Sample Heading");
        elements.push_back(e);
    }

    void parseMarkdown() {
        std::regex headingRegex("^# (.+)$");
        std::regex textRegex("^[^#].+$");
        std::smatch match;

        std::istringstream stream(markDownText);
        std::string line;

        while (std::getline(stream, line)) {
            if (std::regex_match(line, match, headingRegex)) {
                elements.push_back(Element(HEADING, match[1].str()));
            } else if (std::regex_match(line, match, textRegex)) {
                elements.push_back(Element(TEXT, line));
            }
        }
    }


    void convertMarkdownToLatex() {
        std::string latexOutput;
        std::istringstream stream(markDownText);
        std::string line;
        std::vector<std::string> listStack;
        bool inCodeBlock = false;

        while (std::getline(stream, line)) {
            if (line.empty()) {
                latexOutput += "\n";
                continue;
            }

            // Handle code blocks
            if (line.substr(0, 3) == "```") {
                if (inCodeBlock) {
                    latexOutput += "\\end{verbatim}\n";
                    inCodeBlock = false;
                } else {
                    latexOutput += "\\begin{verbatim}\n";
                    inCodeBlock = true;
                }
                continue;
            }

            if (inCodeBlock) {
                latexOutput += line + "\n";
                continue;
            }

            // Handle headings
            std::regex headingRegex("^(#{1,6})\\s+(.+)$");
            std::smatch match;
            if (std::regex_match(line, match, headingRegex)) {
                int level = match[1].length();
                std::string content = match[2];
                if (level == 1) {
                    latexOutput += "\\section{" + content + "}\n";
                } else if (level == 2) {
                    latexOutput += "\\subsection{" + content + "}\n";
                } else if (level == 3) {
                    latexOutput += "\\subsubsection{" + content + "}\n";
                } else if (level == 4) {
                    latexOutput += "\\paragraph{" + content + "}\n";
                } else if (level == 5) {
                    latexOutput += "\\subparagraph{" + content + "}\n";
                } else {
                    latexOutput += "\\textbf{" + content + "}\n";
                }
                continue;
            }

            // Handle lists
            std::regex listRegex("^\\s*([-*+]\\s+|\\d+\\.\\s+)(.+)$");
            if (std::regex_match(line, match, listRegex)) {
                std::string listType = match[1].find_first_of("0123456789") != std::string::npos ? "enumerate" : "itemize";
                std::string content = match[2];

                if (listStack.empty() || listStack.back() != listType) {
                    latexOutput += "\\begin{" + listType + "}\n";
                    listStack.push_back(listType);
                }
                latexOutput += "\\item " + content + "\n";
                continue;
            }

            // Close lists if no longer in a list
            if (!std::regex_match(line, listRegex) && !listStack.empty()) {
                while (!listStack.empty()) {
                    latexOutput += "\\end{" + listStack.back() + "}\n";
                    listStack.pop_back();
                }
            }

            // Handle horizontal rules
            if (std::regex_match(line, std::regex("^(\\*\\*\\*|---|___)$"))) {
                latexOutput += "\\hrulefill\n\n";
                continue;
            }

            // Default case: add the line as is
            latexOutput += line + "\n";
        }

        // Close any remaining open lists
        while (!listStack.empty()) {
            latexOutput += "\\end{" + listStack.back() + "}\n";
            listStack.pop_back();
        }

        std::cout << latexOutput;
    }
}


int main(){
    Element root(HEADING, "Sample Heading");

    Element section(SECTION, "Sample Section");
    Element text(TEXT, "Sample Text");
    section.addChild(text);
    root.addChild(section);

    root.print(); 
}



