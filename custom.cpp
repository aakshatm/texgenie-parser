#include <iostream> 
using namespace std;

enum ElementType{
    HEADING, IMG, TEXT, TABLE, LIST, LINK, CODE, BLOCKQUOTE, HR, HTML, SECTION
};

class Element{
    public: 
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


int main(){
    Element root(HEADING, "Sample Heading");

    Element section(SECTION, "Sample Section");
    Element text(TEXT, "Sample Text");
    section.addChild(text);
    root.addChild(section);

    root.print(); 
}



