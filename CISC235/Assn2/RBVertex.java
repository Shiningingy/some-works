package application;

public class RBVertex {
	int value;
	int colour; //0 for red,1 for black,-1 for leaf.
	RBVertex parent = null;
	RBVertex leftChild;
	RBVertex rightChild;
	
	RBVertex(int value,int colour){//created RBVertex with specific colour
		this.value = value;
		this.colour = colour;
		if(colour == -1) {
			this.leftChild = null;
			this.rightChild = null;
		}
	}
	
	RBVertex(int value){//create a new red RBVertex
		this.value = value;
		this.colour = 0;
		this.leftChild = new RBVertex(0,-1);//attach two leaves
		this.rightChild = new RBVertex(0,-1);
	}
	
	
	
	public String toString() {
		if(colour == 0) {
			return String.valueOf(value) + " red";
		}
		return String.valueOf(value) + " black";
	}

}
