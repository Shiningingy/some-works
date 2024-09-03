package application;

public class Vertex {
	int value;
	Vertex leftChild;
	Vertex rightChild;
	
	Vertex(int value){
		this.value = value;
	}
	
	public String toString() {
		return String.valueOf(value);
	}

}
