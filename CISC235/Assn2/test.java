/*-------------------------------------------
Student:Zili Luo
Student#:20001744

CISC 235
Assignment 2
Programming part
Main function
-------------------------------------------*/
package application;//please put code in application packge in order to run them

public class test {//random function
	public static int[] randomCommon(int min, int max, int n){  
	    if (n > (max - min + 1) || max < min) {  
	           return null;  
	       }  
	    int[] result = new int[n];  
	    int count = 0;  
	    while(count < n) {  
	        int num = (int) (Math.random() * (max - min)) + min;  
	        boolean flag = true;  
	        for (int j = 0; j < n; j++) {  
	            if(num == result[j]){  
	                flag = false;  
	                break;  
	            }  
	        }  
	        if(flag){  
	            result[count] = num;  
	            count++;  
	        }  
	    }  
	    return result;  
	}  
	
	
	public static void main(String[] args) {
		int[] problemsize = {1000,2000,4000,8000,16000};
		int[] vertexValue;
		int[] RtResult= {0,0,0,0,0};//for Rt <0.5,>=0.5 <0.75,>=0.75 <1.25,>=1.25 <1.5,>1.5
		int[] RmResult= {0,0,0,0,0};
		BinaryTree bt;
		RBtree RBt;
		int n;
		float Rt = 0;
		float Rm = 0;
		for(int x = 0;x<5;x++) {
			n = problemsize[x];
			for(int j = 0;j<5;j++) {
				RtResult[j] = 0;
				RmResult[j] = 0;
			}
			for(int y = 0;y<500;y++) {
				vertexValue = randomCommon(0,n,(int) (Math.random() * (n - 1)) + 1);//Generate a random permutation of the set {1,2, ..., n}
				RBt = new RBtree();
				bt = new BinaryTree();
				Rt = 0;
				Rm = 0;
				for(int element:vertexValue) {//insert values
					bt.insertValue(element);
					RBt.insertValue(element);
				}
				Rt = ((float)bt.Total_Depth())/((float)RBt.Total_Depth());//calculate Rt and Rm
				Rm = ((float)bt.Max_Depth())/((float)RBt.Max_Depth());
				if(Rt<0.5) {
					RtResult[0] = RtResult[0]+1;
				}else if(Rt <0.75) {
					RtResult[1] = RtResult[1]+1;
				}else if(Rt<=1.25) {
					RtResult[2] = RtResult[2]+1;
				}else if(Rt<=1.5) {
					RtResult[3] = RtResult[3]+1;
				}else {
					RtResult[4] = RtResult[4]+1;
				}
				
				if(Rm<0.5) {
					RmResult[0] = RmResult[0]+1;
				}else if(Rm <0.75) {
					RmResult[1] = RmResult[1]+1;
				}else if(Rm<=1.25) {
					RmResult[2] = RmResult[2]+1;
				}else if(Rm<=1.5) {
					RmResult[3] = RmResult[3]+1;
				}else {
					RmResult[4] = RmResult[4]+1;
				}
			}//print result
			System.out.println("when n = " + String.valueOf(n) + " RtResult = " + String.valueOf(RtResult[0]) + ","+ String.valueOf(RtResult[1]) + ","+ String.valueOf(RtResult[2]) + ","+ String.valueOf(RtResult[3]) + ","+ String.valueOf(RtResult[4]));
			System.out.println("when n = " + String.valueOf(n) + " RmResult = " + String.valueOf(RmResult[0]) + ","+ String.valueOf(RmResult[1]) + ","+ String.valueOf(RmResult[2]) + ","+ String.valueOf(RmResult[3]) + ","+ String.valueOf(RmResult[4]));
		}
		//test codes
		/*
		System.out.println("run test code for normal binary tree");
		BinaryTree bt = new BinaryTree();
		bt.insertValue(6);
		bt.insertValue(10);
		bt.insertValue(20);
		bt.insertValue(8);
		bt.insertValue(3);
		System.out.println("searchPath");
		bt.searchPath(8);
		System.out.println("totalDepath" + String.valueOf(bt.Total_Depth()));
		System.out.println("maxDepath "+ String.valueOf(bt.Max_Depth()));
		System.out.println("run test code for R-B binary tree");
		RBtree RBt = new RBtree(6);
		RBt.insertValue(10);
		RBt.insertValue(20);
		RBt.insertValue(8);
		RBt.insertValue(3);
		System.out.println("normal insert finished");
		System.out.println("searchPath");
		RBt.searchPath(8);
		System.out.println("totalDepath" + String.valueOf(RBt.Total_Depth()));
		System.out.println("maxDepath "+ String.valueOf(RBt.Max_Depth()));
		RBt = new RBtree();
		RBt.insertValue(6);
		RBt.insertValue(1);
		RBt.insertValue(10);
		RBt.insertValue(20);
		RBt.insertValue(30);
		System.out.println("single rotation insert finished");
		System.out.println("searchPath");
		RBt.searchPath(30);
		System.out.println("totalDepath " + String.valueOf(RBt.Total_Depth()));
		System.out.println("maxDepath "+ String.valueOf(RBt.Max_Depth()));
		RBt = new RBtree();
		RBt.insertValue(6);
		RBt.insertValue(10);
		RBt.insertValue(8);
		RBt.insertValue(20);
		RBt.insertValue(3);
		System.out.println("double rotation insert finished");
		System.out.println("searchPath");
		RBt.searchPath(20);
		System.out.println("totalDepath " + String.valueOf(RBt.Total_Depth()));
		System.out.println("maxDepath "+ String.valueOf(RBt.Max_Depth()));
		*/
	}
}
