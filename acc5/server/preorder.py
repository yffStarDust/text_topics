##defination for a binary tree
class TreeNode(object):
    def __init__(self,x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
     def iterative_preorder(self,root,list):
         stack = []
         while root or stack:
             if root:
                 list.append(root.val)
                 stack.append(root)
                 root=root.left
             else:
                 root=stack.pop()
                 root=root.right
         return list

     def recruisive_preorder(self,root,list):
         if root:
             list.append(root.val)
             self.recruisive_preorder(root.left,list)
             self.recruisive_preorder(root.right,list)

     def preorder_Traversal(self,root):
         list = []
         self.iterative_preorder(root,list)
         return list


class BinaryTree(object):
    def __init__(self):
        self.root = Node()

    def add(self, data):
        node = Node(data)
        if self.isEmpty():
            self.root = node
        else:
            tree_node = self.root
            queue = []
            queue.append(self.root)

            while queue:
                tree_node = queue.pop(0)
                if tree_node.lchild == None:
                    tree_node.lchild = node
                    return
                elif tree_node.rchild == None:
                    tree_node.rchild = node
                    return
                else:
                    queue.append(tree_node.lchild)
                    queue.append(tree_node.rchild)






