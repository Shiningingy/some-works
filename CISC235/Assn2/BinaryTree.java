package application;

public class BinaryTree {
	private Vertex root = null;
	private int totalpath = 0;
	private int maxpath = 0;
	
	BinaryTree(int value){
		root = new Vertex(value);
		root.leftChild = null;
		root.rightChild = null;
	}
	
	BinaryTree(){
		root = null;
	}
	
	//insertFunction
	public void insertValue(int value){
		Vertex newVertex = new Vertex(value);
		if(root == null) {
			root = newVertex;
			root.leftChild = null;
			root.rightChild = null;
		}else {
			Vertex current = root;
			while(true) {
				if (value < current.value) {
					if(current.leftChild == null) {
						current.leftChild = newVertex;
						break;
					}else {
						current = current.leftChild;
					}
				}else {//since assume the value stored in binary tree are unique
					//i don't consider the error case which inserted value is already in the tree
					if(current.rightChild == null) {
						current.rightChild = newVertex;
						break;
					}else {
						current = current.rightChild;
					}
				}
			}
		}
	}
	
	//searchPath Function
	public void searchPath (int value) {
		Vertex current = root;
		while(true) {
			System.out.println(current.toString());
			if(value < current.value) {
				if(current.leftChild == null) {
					System.out.println("The value is not in the tree");
				}else {
					current = current.leftChild;
				}
			}else if(value > current.value) {
				if(current.rightChild == null) {
					System.out.println("The value is not in the tree");
				}else {
					current = current.rightChild;
				}
			}else {
				break;
			}
		}
	}
	
	
	//totalPath Function
	public int Total_Depth() {
		totalpath = 0;
		Total_Depth(root,1);
		return totalpath;
	}
	
	private void Total_Depth(Vertex current,int path) {
		if(current == null) {
			return ;
		}
		totalpath = totalpath + path;
		Total_Depth(current.leftChild,path+1);
		Total_Depth(current.rightChild,path+1);
	}
	
	
	//maxPath
	public int Max_Depth() {
		maxpath = 0;
		Max_Depth(root,1);
		return maxpath;
	}
	
	private void Max_Depth(Vertex current,int path) {
		if(current == null) {
			return ;
		}
		if(maxpath < path) {
			maxpath = path;
		}
		Max_Depth(current.leftChild,path+1);
		Max_Depth(current.rightChild,path+1);
	}
	
	
	
}

