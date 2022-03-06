import java.util.ArrayList;

public class Factor {

	public static double[] varArray(double[][] inputData) {
		// TODO Auto-generated method stub
		ArrayList al = new ArrayList();
		for(int i=0;i<inputData.length;i++){
			al.add(""+inputData[i][3]);
		}
		
		
		double min=Double.parseDouble(""+al.get(0)); 
		for(int i=0;i<al.size();i++){ 
			 if(Double.parseDouble(""+al.get(i))<min) 
			 min=Double.parseDouble(""+al.get(i)); 
			} 
		
		double max=Double.parseDouble(""+al.get(0)); 
		for(int i=0;i<al.size();i++){ 
			 if(Double.parseDouble(""+al.get(i))>max) 
			 max=Double.parseDouble(""+al.get(i)); 
			} 
		
		
		double[] varArray = new double[al.size()];
		double sum=(max-min);
		double sum1=0;
		for(int i=0;i<al.size();i++){
			sum1=(Double.parseDouble(""+al.get(i)))-min;
			varArray[i] =sum1/sum;
		}
		
	
		return varArray;
	}

}
