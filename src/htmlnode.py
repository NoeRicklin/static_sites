from functools import reduce
from sys import exit


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child hasn't overwritten self.to_html()")
    
    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        props_str = reduce(lambda cur_str, key: cur_str + f' {key}="{self.props[key]}"', self.props, "")
        return props_str
    
    def __repr__(self):
        htmlnode_str = f'HTMLNode:\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props_to_html()}'
        return htmlnode_str
    
    def __eq__(self, other):
        return self.__repr__() == other.__repr__()


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("No Value in leaf node")
        if self.tag == None:
            return self.value

        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"

        html_repr = opening_tag + self.value + closing_tag
        return html_repr


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No Tag in parent node")
        if self.children == None or self.children == []:
            raise ValueError("No children in parent node")
        
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"

        children_html = "".join(map(lambda child: child.to_html(), self.children))
        html_repr = opening_tag + children_html + closing_tag
        return html_repr

