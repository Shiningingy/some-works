package application;

public class RBtree {
	private RBVertex root = null;
	private int totalpath = 0;
	private int maxpath = 0;
	
	RBtree(int value){
		this.root = new RBVertex(value);
		this.root.colour = 1;
	}
	
	RBtree(){
		this.root = null;
	}
	
	//insertFunction
	public void insertValue(int x){
		this.root = RBinsert(root,x);
		this.root.colour = 1;//set root colour to black
	}
	
	//recursive insert
	private RBVertex RBinsert(RBVertex current,int x) {
		if(current == null || current.colour == -1) {//if current is a leaf or is a empty tree
			return new RBVertex(x);//create a red vertex and give it two leaves
		}else if(current.value > x) {
			current.leftChild = RBinsert(current.leftChild,x);
			if(current.leftChild.colour == 1) {
				return current;
			}else {
				if(current.leftChild.leftChild.colour == 0 || current.leftChild.rightChild.colour == 0) {
					if(current.leftChild.leftChild.colour == 0) {
						return Left_Left_fix(current);
					}else {
						return Left_Right_fix(current);
					}
				}else {
					return current;
				}
			}
		}else {
			current.rightChild = RBinsert(current.rightChild,x);
			if(current.rightChild.colour == 1) {
				return current;
			}else {
				if(current.rightChild.leftChild.colour == 0 || current.rightChild.rightChild.colour == 0) {
					if(current.rightChild.leftChild.colour == 0) {
						return Right_Left_fix(current);
					}else {
						return Right_Right_fix(current);
					}
				}else {
					return current;
				}
			}
		}
	}
	
	//fix function
	private RBVertex Left_Left_fix(RBVertex GP) {
		RBVertex Parent = GP.leftChild;
		RBVertex Sibling = GP.rightChild;
		if(Sibling.colour == 0) {
			Parent.colour = 1;
			Sibling.colour = 1;
			GP.colour = 0;
			return GP;
		}else {
			GP.leftChild = Parent.rightChild;
			Parent.rightChild = GP;
			Parent.colour = 1;
			GP.colour = 0;
			return Parent;
		}
	}
	
	private RBVertex Left_Right_fix(RBVertex GP) {
		RBVertex Parent = GP.leftChild;
		RBVertex Sibling = GP.rightChild;
		if (Sibling.colour == 0) {
			Parent.colour = 1;
			Sibling.colour = 1;
			GP.colour = 0;
			return GP;
		}else {
			RBVertex current = Parent.rightChild;
			Parent.rightChild = current.leftChild;
			GP.leftChild = current.rightChild;
			current.leftChild = Parent;
			current.rightChild = GP;
			current.colour = 1;
			GP.colour = 0;
			return current;
		}
	}
	
	private RBVertex Right_Left_fix(RBVertex GP) {
		RBVertex Parent = GP.rightChild;
		RBVertex Sibling = GP.leftChild;
		if (Sibling.colour == 0) {
			Parent.colour = 1;
			Sibling.colour = 1;
			GP.colour = 0;
			return GP;
		}else {
			RBVertex current = Parent.leftChild;
			Parent.leftChild = current.rightChild;
			GP.rightChild = current.leftChild;
			current.rightChild = Parent;
			current.leftChild = GP;
			current.colour = 1;
			GP.colour = 0;
			return current;
		}
	}
	
	private RBVertex Right_Right_fix(RBVertex GP) {
		RBVertex Parent = GP.rightChild;
		RBVertex Sibling = GP.leftChild;
		if(Sibling.colour == 0) {
			Parent.colour = 1;
			Sibling.colour = 1;
			GP.colour = 0;
			return GP;
		}else {
			GP.rightChild = Parent.leftChild;
			Parent.leftChild = GP;
			Parent.colour = 1;
			GP.colour = 0;
			return Parent;
		}
	}
	
	
	
	//searchPath Function
	public void searchPath (int value) {
		RBVertex current = root;
		while(true) {
			System.out.println(current.toString());
			if(value < current.value) {
				if(current.leftChild.colour == -1) {
					System.out.println("The value is not in the tree");
					break;
				}else {
					current = current.leftChild;
				}
			}else if(value > current.value) {
				if(current.rightChild.colour == -1) {
					System.out.println("The value is not in the tree");
					break;
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
	
	private void Total_Depth(RBVertex current,int path) {
		if(current.colour == -1) {
			return;
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
	
	private void Max_Depth(RBVertex current,int path) {
		if(current == null || current.colour == -1) {
			return ;
		}
		if(maxpath < path) {
			maxpath = path;
		}
		Max_Depth(current.leftChild,path+1);
		Max_Depth(current.rightChild,path+1);
	}


}
