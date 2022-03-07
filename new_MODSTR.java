import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.List;


public class new_MODSTR {
	public static void main(String[] args) throws IOException{
		int chooseReturnRate=15;
		int chooseMDD=0;
		int choosecount=0;
		int part=100;//幾個1
		
		int K = 3; //將股票分為K群, 目前可以跑的有K= 3, 4, 5, 6都可以正常運作
		int maxCaptial = 100000;
		int pSize = 10; // popuation size
		int numberofST= chooseReturnRate+chooseMDD+choosecount;
		int generation = 100; 
		double crossoverRate = 0.8;
		double mutationRate = 0.03;
		double inversionRate = 0.6;
		
		String Training[]=null;
		String Testing[]=null;
		
		String Training1[]=null;
		String Testing1[]=null;
		
		for(int tr=1;tr<=3;tr++){
			if(tr==1){
				Training=new String[]{"2011-2013.txt", "2012-2014.txt", "2013-2015.txt"};
				Testing=new String[]{"2014.txt", "2015.txt", "2016.txt"};
			}
			if(tr==2){
				Training=new String[]{"2011-2012.txt", "2012-2013.txt", "2013-2014.txt", "2014-2015.txt"};
				Testing=new String[]{"2013.txt", "2014.txt", "2015.txt", "2016.txt"};
			}
			if(tr==3){
				Training=new String[]{"2011.txt", "2012.txt", "2013.txt", "2014.txt", "2015.txt"};
				Testing=new String[]{"2012.txt", "2013.txt", "2014.txt", "2015.txt", "2016.txt"};
			}
			
		/*	
		Training=new String[]{"2012.txt", "2013.txt", "2014.txt", "2015.txt"};
		Testing=new String[]{"2013.txt", "2014.txt", "2015.txt", "2016.txt"};
		*/
			for(int trte=0; trte<Testing.length;trte++){ // trte = traning & testing
				String fileTEC =  Training[trte];
				String TestfileTEC = Testing[trte];

				int num=readTECInputData(fileTEC);//讀training的有幾天
				int num1=readTECInputData(TestfileTEC);//讀TESTING有幾天
				String[][] inputDataTEC = readTECInputData1(fileTEC, num);//讀training幾年的所有資料
				String[][] inputTestfileTEC = readTECInputData1(TestfileTEC, num1);//讀testing幾年的所有資料
				long startTime = System.currentTimeMillis(); // 取得現在的時間 (毫秒) 

				double[] a=new double[20];
				double[] b=new double[20];
				double[] c=new double[20];
				double[] d=new double[20];
				
				double STOPPP[]={0.0, 0.05, 0.10, 0.15, 0.05, 0.05, 0.10, 0.15, 0.15}; // 停利點
				double STOPLOSE[]={0.0, -0.05, -0.10, -0.15, -0.10, -0.15, -0.05, -0.05, -0.10}; // 停損點
				Hashtable<String,Hashtable> input = new Hashtable<String,Hashtable>();
				Hashtable<String,Hashtable> input1= new Hashtable<String,Hashtable>();
				
				for(int C=0;C<=8;C++){
					input=pop(STOPPP[C],STOPLOSE[C],inputDataTEC, inputTestfileTEC, num,chooseReturnRate,chooseMDD,choosecount,num1,input);
					input1=pop1(STOPPP[C],STOPLOSE[C],inputDataTEC, inputTestfileTEC, num,chooseReturnRate,chooseMDD,choosecount,num1,input1);//加交易稅的
				}
				for(int C=0;C<=8;C++){
				
					BufferedWriter Finalr = new BufferedWriter(new FileWriter("Final"+"["+ STOPPP[C]+","+STOPLOSE[C]+"]"+Testing[trte]+"("+Training[trte]+").txt"));
					
					for(int r=0;r<10;r++){
						String s = Integer.toString(r);
						BufferedWriter br = new BufferedWriter(new FileWriter("FinalResult"+"["+ STOPPP[C]+","+STOPLOSE[C]+"]"+Testing[trte]+"("+Training[trte]+")"+r+".txt"));
						String txt="initialChromosome"+r+".txt";
						File f = new File(txt);
						Hashtable<String, chromosome> population;

						if(!f.exists()){
							population = generateInitialPopulation(pSize,numberofST, K , part);
							outPutInitialChromosome(population, f,K);
							printPopulation(population);
						}
						else{
							population = readInitialChromosome(f, K);
							printPopulation(population);
						}
						population = calculateFitnessValue(population, input, maxCaptial, STOPPP[C],STOPLOSE[C]);
						writeExperimentValuetoFile(population, br, 0, System.currentTimeMillis() - startTime);

						for(int i=0; i<generation; i++){
							population = executeSelectionOperator(population, pSize);
							printPopulation(population);
							if(i == generation-1){
								if(C(population,findbestChromosome(population))){
									System.out.println("FinalBest");
									double first=printAChromosome(population, findbestChromosome(population), input, Finalr,maxCaptial, STOPPP[C],STOPLOSE[C]);
									a[r]=first;
									double secound[]=printAChromosome1(population, findbestChromosome(population),input, Finalr,maxCaptial, STOPPP[C],STOPLOSE[C]);

									b[r]=secound[0];//平均
									c[r]=secound[1];//最大
									d[r]=secound[2];//最小
									writeExperimentValuetoFile(population, br, i, System.currentTimeMillis() - startTime);
									br.close();
								}
								else{
									f.delete();
									/*population = generateInitialPopulation(pSize,inputData, K);
									outPutInitialChromosome(population, f,K);*/
									r--;
								}
							}
							else if (i%5 == 0 && i!=0){
								writeExperimentValuetoFile(population, br, i, System.currentTimeMillis()- startTime);
							}
							
							population = executeCrossoverOperator(population, crossoverRate,K);
				//			printPopulation(population);

							population = executeMutationOperator(population, mutationRate, pSize, K);
							printPopulation(population);
							population = executeInversionOperator(population, inversionRate, pSize);

							System.out.print("input.size()"+input.size());
					
							population = calculateFitnessValue(population, input, maxCaptial, STOPPP[C],STOPLOSE[C] );
						}
						population.clear();
					}
					//加交易稅
						for(int r=10;r<20;r++){
				//			String s = Integer.toString(r);
							BufferedWriter br = new BufferedWriter(new FileWriter("FinalResult"+"["+ STOPPP[C]+","+STOPLOSE[C]+"]"+Testing[trte]+"("+Training[trte]+")"+r+".txt"));
							String txt="initialChromosome"+r+".txt";
							File f = new File(txt);
							Hashtable<String, chromosome> population;
							if(!f.exists()){
								population = generateInitialPopulation(pSize,numberofST, K , part);
								outPutInitialChromosome(population, f,K);
								printPopulation(population);
							}else{
								population = readInitialChromosome(f, K);
								printPopulation(population);
							}
							population = calculateFitnessValue(population, input1, maxCaptial, STOPPP[C],STOPLOSE[C]);
							writeExperimentValuetoFile(population, br, 0, System.currentTimeMillis() - startTime);
					
								
							for(int i=0; i<generation; i++){
								population = executeSelectionOperator(population, pSize);
								printPopulation(population);
								if(i == generation-1){
									if(C(population,findbestChromosome(population))){
										System.out.println("FinalBest");
										double first=printAChromosome(population, findbestChromosome(population), input1, Finalr,maxCaptial, STOPPP[C],STOPLOSE[C]);
										a[r]=first;
										double secound[]=printAChromosome1(population, findbestChromosome(population),input1, Finalr,maxCaptial, STOPPP[C],STOPLOSE[C]);
										
										b[r]=secound[0];//平均
										c[r]=secound[1];//最大
										d[r]=secound[2];//最小
										writeExperimentValuetoFile(population, br, i, System.currentTimeMillis() - startTime);
										br.close();
									}
									else{
										f.delete();
										/*population = generateInitialPopulation(pSize,inputData, K);
										outPutInitialChromosome(population, f,K);*/
										r--;
									}
								}else if (i%5 == 0 && i!=0){
										writeExperimentValuetoFile(population, br, i, System.currentTimeMillis()- startTime);
								}
								

								population = executeCrossoverOperator(population, crossoverRate,K);

					//			printPopulation(population);

								population = executeMutationOperator(population, mutationRate, pSize, K);
								printPopulation(population);
								
								population = executeInversionOperator(population, inversionRate, pSize);
								
								System.out.print("input.size()"+input1.size());
						
								population = calculateFitnessValue(population, input1, maxCaptial, STOPPP[C],STOPLOSE[C] );
							}

						}

						double avg1=0;
						double avg2=0;
						double avg3=0;
						double avg4=0;

						Finalr.newLine();
						double Maxnum[] = new double[10];
						
						double Minnum[] = new double[10];
						double avgnum[] = new double[10];
						double three1[] = new double[3];
				
					for(int i=0;i<10;i++){
						System.out.printf("%f",a[i]);///first
						System.out.printf(",%f",b[i]);//AVG
						System.out.printf(",%f",c[i]);//MAX
						System.out.printf(",%f",d[i]);//min
						
						Finalr.write("first="+a[i]+"AVG="+b[i]+"  MAX= "+c[i]+"  min="+d[i]);
						Finalr.newLine();
						avg1=avg1+a[i];
						avg2=avg2+b[i];//平均
						avg3=avg3+c[i];//最大
						avg4=avg4+d[i];//最小
					
						Maxnum[i] =c[i];
						Minnum[i]=d[i];
						avgnum[i] =b[i];
				}
				
					DecimalFormat df = new DecimalFormat("#0.00");
					df.setRoundingMode(RoundingMode.HALF_UP);
					
					DecimalFormat df1 = new DecimalFormat("#0.000");
					df1.setRoundingMode(RoundingMode.HALF_UP);
					
					System.out.printf("%.2f,%.2f,%.2f",avg1/10,avg2/10,(avg3/10)/(avg4/10));
					String one = String.valueOf(df.format(avg1/10));
					String two = String.valueOf( df.format(avg2/10));
					String three = String.valueOf( df.format((avg3/10)));
					String four = String.valueOf( df.format(avg4/10));
			
	/*	for(int ggg=0;ggg<10;ggg++){
			Finalr.write("ggg"+Maxnum[ggg]);
		}*/
					Finalr.newLine();

					Finalr.newLine();
					Finalr.write("first="+one+"AVG="+two+" MAX="+three+" min="+four);
					Finalr.newLine();
					
					three1[0]=(avg2/10)*100;
					three1[1]=(avg3/10)*100;
					three1[2]=(avg4/10)*100;
					
					double variance1=va(avgnum,three1[0]);
					double variance2=va(Maxnum,three1[1]);
					double variance3=va(Minnum,three1[2]);
					
					Finalr.write("gog"+(avg3/10));
					Finalr.newLine();
					Finalr.write("AVGVAR="+ variance1+"  MAXVAR="+ variance2+"  MinVAR="+ variance3);
					Finalr.newLine();
					Finalr.newLine();
					Finalr.newLine();
					System.out.println("");
					System.out.println("");
					System.out.println("");
					avg1=0;
					avg2=0;
					avg3=0;
					avg4=0;
					

					for(int i=10;i<20;i++){
						System.out.printf("%f",a[i]);///first
						System.out.printf(",%f",b[i]);//AVG
						System.out.printf(",%f",c[i]);//MAX
						System.out.printf(",%f",d[i]);//min.
						
						Finalr.write(a[i]+"AVG="+b[i]+"  MAX= "+c[i]+"  min="+d[i]);
						Finalr.newLine();
						
						avg1=avg1+a[i];//Final best traning
						avg2=avg2+b[i];//平均
						avg3=avg3+c[i];//最大
						avg4=avg4+d[i];//最小
						
						Maxnum[i-10] =c[i];
						Minnum[i-10]=d[i];
						avgnum[i-10] =b[i];
					}
						
					System.out.printf("%.2f,%.2f,%.2f",avg1/10,avg2/10,(avg2/10)/(avg3/10));
					one = String.valueOf( df.format(avg1/10));
					two = String.valueOf(df.format(avg2/10));
					three =String.valueOf( df.format(avg3/10));
					four=String.valueOf( df.format(avg4/10));
					
					Finalr.write(one+"AVG="+two+" MAX="+three+" min="+four);
					Finalr.newLine();
					
					variance1=va(avgnum,((avg2/10)*100));
					variance2=va(Maxnum,((avg3/10)*100));
					variance3=va(Minnum,((avg4/10)*100));
					
					Finalr.newLine();
					Finalr.write("AVGVAR= "+ variance1+"  MAXVAR="+ variance2+"  MinVAR="+ variance3);
					Finalr.newLine();
					System.out.println("-------------------------------------------------------------------------------------");
					Finalr.write("-------------------------------------------------------------------------------------");
					Finalr.newLine();
					Finalr.close();
					
					for(int r=0;r<20;r++){
						String rrr="initialChromosome"+r+".txt";
						File fi = new File(rrr);
						fi.delete();
					}
				}
			}
		}
	}
	
	static int findbestChromosome(Hashtable<String, chromosome> chro){
		int maxIndex = 0;
		double maxFitValue=-10000000;
		
		for(Enumeration e = chro.keys(); e.hasMoreElements();){
			String num = (String)e.nextElement();
			if(chro.get(num).fitness[0]>maxFitValue){
				maxFitValue = chro.get(num).fitness[0];
				maxIndex=Integer.parseInt(num);
			//	System.out.println("maxIndex=" + maxIndex+ " maxFitValue="+maxFitValue);	
			}
		}
		//System.out.println("maxIndex=" + maxIndex);
		
		return maxIndex;
	}	
	private static Hashtable<String, Hashtable> pop( double stopPP, double stoplose, String[][] inputDataTEC, String[][] inputTestfileTEC, int num, int chooseReturnRate, int chooseMDD, int choosecount,int num1, Hashtable<String, Hashtable> input) {
		// TODO Auto-generated method stub
		//System.out.println(num);
		double RankReturnRate[]=new double[100]; // ranking returnrate
		double Rank1ReturnRate[]=new double[100];// same
		double Rank1[][]=new double[100][6];
		double RankMDD[]=new double[100];		//ranking MDD
		double Rank1MDD[]=new double[100];		//same
		double Rankcount[]=new double[100];		//ranking count
		double Rank1count[]=new double[100];
		int co = 7;

		String stopp=stopPP+","+stoplose; // 沒用
		System.out.println( "*&**"+stopPP+","+stoplose);

		ArrayList<Integer> alre =new ArrayList<>(); //
		while(co!=107){
			//System.out.println(co+","+"co");
			ArrayList<String[]>str= STR11(inputDataTEC, num,co,stopPP,stoplose);
			if(stopPP==0.0 && stoplose==-0.0){
				str= STR(inputDataTEC, num,co);
			}

			for(int i=0;i<str.size();i++){
				String aaa[]=str.get(i);
			//System.out.println(aaa[1]+" "+aaa[2]+" "+aaa[3]);
			}

			if(str.size()==0){
				//System.out.println("NULL");
				RankReturnRate[co-7]=-999999;
				RankMDD[co-7]=-999999;
				Rankcount[co-7]=999999;
				Rank1ReturnRate[co-7]=co-6;
				Rank1MDD[co-7]=co-6;
				Rank1count[co-7]=co-6;
				
				//Rank1[co-46][1]=ReturnRate;
				Rank1[co-7][0]=co-6;
				Rank1[co-7][1]=-999999;
				Rank1[co-7][2]=-999999;
				Rank1[co-7][3]=999999;
				Rank1[co-7][4]=-999999;
				Rank1[co-7][5]=-999999;
			}
			else{
				int Count =count(str);
				double ReturnRate=mareturnrate(str);
				double ReturnRate1=mareturnrate1(str);
				double MDD=MDD(str,Count);//價差取最大客略虧損
				double MDD1=MDD1(str,Count);//以前的
			 
			//System.out.println(num+","+Count+","+Return+","+Return1+","+ReturnRate+","+ReturnRate1+","+PPT+","+PPT1+","+count1+","+count2+","+WinRate+","+WinRate1+","+WinAve+","+WinAve1+","+LosAve+","+LosAve1+","+MDD+","+tax+","+onceReturnRate);
			//System.out.println("OOO"+PF);
				RankReturnRate[co-7]=ReturnRate;
				RankMDD[co-7]=MDD;
				Rankcount[co-7]=Count;
				Rank1ReturnRate[co-7]=co-6;
				Rank1MDD[co-7]=co-6;
				Rank1count[co-7]=co-6;
				
				//Rank1[co-46][1]=ReturnRate;
				Rank1[co-7][0]=co-6;//第幾個策略
				Rank1[co-7][1]=ReturnRate;
				Rank1[co-7][2]=MDD;
				Rank1[co-7][3]=Count;
				Rank1[co-7][4]=ReturnRate1;
				Rank1[co-7][5]=MDD1;
				 System.gc();
			}
			co++;
		}
		for (int i =  RankReturnRate.length - 1; i > 0; --i)
			for (int j = 0; j < i; ++j)
				if (RankReturnRate[j] < RankReturnRate[j + 1]){
					Swap(RankReturnRate, j, j + 1);
					alre=RReturnRate(RankReturnRate,Rank1ReturnRate,chooseReturnRate,alre);
					System.gc();
					double Rank1bMDD[]=new double[RankMDD.length-alre.size()];
					double RankbMDD[]=new double[RankMDD.length-alre.size()];

					int c=0;
					for(int i=0;i<Rank1MDD.length;i++){
						if(alre.contains((int)(Rank1MDD[i])))
								continue;
						else{
							Rank1bMDD[c]=Rank1MDD[i];
							RankbMDD[c]=RankMDD[i];
							c++;
						}
					}
					for (int i =  RankbMDD.length - 1; i > 0; --i)
						for (int j = 0; j < i; ++j)
							if ( RankbMDD[j] < RankbMDD[j + 1]){
								Swap(RankbMDD, j, j + 1);
								Swap(Rank1bMDD, j, j + 1);
							}
					alre=RReturnRate(RankbMDD,Rank1bMDD,chooseMDD,alre);
					double Rank1bcount[]=new double[Rankcount.length-alre.size()];
					double Rankbcount[]=new double[Rankcount.length-alre.size()];
					int d=0;
					for(int i=0;i<Rank1count.length;i++){
						if(alre.contains((int)(Rank1count[i])))
								continue;
						else{
							Rank1bcount[d]=Rank1count[i];
							Rankbcount[d]=Rankcount[i];
							d++;
						}
					}
		 	 	 	for (int i =  Rankbcount.length - 1; i > 0; --i)
		 				for (int j = 0; j < i; ++j)
							if ( Rankbcount[j] > Rankbcount[j + 1]){
								Swap(Rankbcount, j, j + 1);
								Swap(Rank1bcount, j, j + 1);
							}
		 	 	 	alre=RReturnRate1(Rankbcount,Rank1bcount,choosecount,alre);
					System.out.println(alre);
					double storea[][]=new double[alre.size()][4];
					double storeb[][]=new double[alre.size()][4];
					
					Hashtable<String,double[][]> store = new Hashtable<String,double[][]>();

					for(int i=0;i<alre.size();i++){
						co=alre.get(i);//第幾個策略(從15個策略選出)
						storea[i][0]=co;//第幾個策略
						storea[i][1]=Rank1[co-1][3];
						storea[i][2]=Rank1[co-1][1];
						storea[i][3]=Rank1[co-1][2];
						if(storea[i][1]==999999||storea[i][2]==-999999||storea[i][3]==-999999){
							storea[i][0]=co;//第幾個策略
							storea[i][1]=0;
							storea[i][2]=0;
							storea[i][3]=0;
						}
						co=co+6;
						// System.out.println(co+","+"co11");
						ArrayList<String[]>str1= STR11(inputTestfileTEC, num1,co,stopPP,stoplose);
						if(Double.valueOf(stopPP)==0.00 && Double.valueOf(stoplose)==-0.00){
							str1= STR(inputTestfileTEC, num1,co);
						}
						if(str1.size()==0){
							storeb[i][0]=co-6;//第幾個策略(1-15)
							storeb[i][1]=0;
							storeb[i][2]=0;
							storeb[i][3]=0;
						}
						else{
							int Count =count(str1);
							double ReturnRate=mareturnrate(str1);
							double ReturnRate1=mareturnrate1(str1);
							double MDD=MDD(str1,Count);//價差取最大策略虧損
							double MDD1=MDD1(str1,Count);//價差取最大策略虧損-tax
							storeb[i][0]=co-6;
							storeb[i][1]=Count;
							storeb[i][2]=ReturnRate;
							storeb[i][3]=MDD;
						}
					}

	//		String Point=population.get(""+p).point.get(1)+","+stoplose;
					store.put(""+0,storea);
					store.put(""+1,storeb);
					input.put(""+stopp,store);
					Enumeration<String> e = input.keys();
					while(e. hasMoreElements()){
						String s= e.nextElement().toString();
						Hashtable s2 = input.get(s);
						System.out.println(s);
					}
					return input;
				}
	}
	private static void Swap(double[] rank, int indexA, int indexB){
		double tmp = rank[indexA];
		rank[indexA] = rank[indexB];
		rank[indexB] = tmp;
	}

	public static int readTECInputData(String fileName) {//讀出有幾天
		int i=0;
		try{
			BufferedReader br =  new BufferedReader(new FileReader(fileName));
			String st = "";
			while((st=br.readLine())!=null){
				i++;
			}
			br.close();	
		}catch(Exception e){}
		return i;
	}

	public static String[][] readTECInputData1(String fileTEC, int num) {//所有資料存起來
		//System.out.println(num);
		String[][] inputData = new String[num][107];
		
		try{
			int i=0;
			BufferedReader br =  new BufferedReader(new FileReader(fileTEC));
			String st = "";
			while((st=br.readLine())!=null){
				String[] a = st.split("	");
				for(int j=0;j<107;j++){
					inputData[i][j] = a[j];
				}
				i++;
			}
			br.close();
		}catch(Exception e){}
		return inputData;
	}
	
	
	private static Hashtable<String, chromosome> generateInitialPopulation(int pSize,int numberofST, int K, int part) {
		Hashtable<String, chromosome> population = new Hashtable<String, chromosome>();
		ArrayList AL = new ArrayList();
			//substep1.1: Randomly generate grouping part according to number of groups K
	//		int numberofStock = inputData.length;
			for(int i=0; i<pSize; i++){
				chromosome chro =  new chromosome();
				for(int j=0; j<numberofST; j++){
					int groupNum = (int) (Math.random()*1000)%K;
					//System.out.println(groupNum);
					if(!chro.groupPart.containsKey(""+groupNum))
						chro.groupPart.put(""+groupNum, j+",");
					else
						chro.groupPart.put(""+groupNum, chro.groupPart.get(""+groupNum).toString()+j+",");
				}
				if(check_K_NonEmptyGroup(chro, K)){
					i--;
				}else{
					population.put(""+i, chro);
				//	System.out.println("aa"+chro.groupPart);
				}
				
			}
			//Weight part
			for(int t=0; t<pSize; t++){
				int[] R = new int [K];
				int i=0;
				int value=0;
				while(i<K){//隨機K個不同的亂數
					if(i==0){
						R[i] = (int) (Math.random()*(K+part));
					}else{
						value = (int) (Math.random()*(K+part));
						for(int j=0;j<i;j++){
							if(value==R[j]){
								j=-1;
								value = (int) (Math.random()*(K+part));
							}
						} //驗證value 是否已存在
						R[i]=value; 
					}
					i++;
				}
				int count=0;
				String weight="";
				for(int s=0;s<(K+part);s++){
					for(int j=0;j<R.length;j++){
						if(s==R[j]){
							count++;
						}
					}
					if(count==1){
						weight=weight+"0";
					}
					else
						weight=weight+"1";
					count=0;
				}// 用0 區分 k 群的權重
		//	AL.add(weight);
				int count1=0;
				double[] CO=new double[K+1]; //個別weight 的長度
				String a=weight;
					
				String[] aa=a.split("0");
				for(int o=0;o<aa.length;o++){
					count1=(aa[o].length());
					CO[o]=count1;
				}
				population.get(""+t).strategyweight.add(weight);

				for(int u=0;u<K+1;u++){
					population.get(""+t).strategyweight.add(( (part/(a.length()-K)) *CO[u])/part); // 個別的 %
					//=>> 個別的長度 / part
				}
			 
			}

		return population;

	}
		
	static boolean check_K_NonEmptyGroup(chromosome chro, int K) {
		boolean flag = false;
		if(chro.groupPart.size()!=K) flag = true ; //等於的話會回傳false,不等於回傳true (me)
		return flag;
	}
	private static void outPutInitialChromosome(Hashtable<String, chromosome> population, File f, int K) {
		 BufferedWriter bw;
		 try{
			bw =  new BufferedWriter(new FileWriter(f));
			for(int i=0; i<population.size(); i++){
				for(int j=0; j<population.get(""+i).groupPart.size(); j++){
					bw.write(""+population.get(""+i).groupPart.get(""+j));
					bw.newLine();
				}
				for(int j=0; j<population.get(""+i).strategyweight.size(); j++){
					bw.write(""+population.get(""+i).strategyweight.get(j)+",");
				}
				bw.newLine();
			}
			 bw.close();
		 }catch(Exception e ){
		 }
	}
	
	private static void printPopulation(Hashtable<String, chromosome> population) {
//			System.out.println("population.size()= "+population.size());
		for(int i=0; i<population.size(); i++){	
			for(int j=0; j<population.get(""+i).groupPart.size(); j++){
				System.out.print(population.get(""+i).groupPart.get(""+j)+" ");
			}
			
			for(int j=0; j<population.get(""+i).strategyweight.size(); j++){
				System.out.print(population.get(""+i).strategyweight.get(j)+" ");
			}
			System.out.println();
		}
	}
	
	private static Hashtable<String, chromosome> readInitialChromosome(File f, int K) {
		BufferedReader br;
		Hashtable<String, chromosome> pop = new Hashtable<String, chromosome>();
		try{
			br = new BufferedReader(new FileReader(f));
			String st="";
			int chroNum = 0;
			int lineCount = 0;
			chromosome chro = new chromosome();
			
			while((st = br.readLine())!=null){
				if(lineCount != K ){
					chro.groupPart.put(""+lineCount, st);
				//	System.out.println(st);
					lineCount++;
				}else{
					String[] stArr = st.split(",");
					for(int k = 0; k<stArr.length; k++)
						chro.strategyweight.add(stArr[k]);
					
					pop.put(""+chroNum, chro);
					chroNum++;
					chro = new chromosome();
					lineCount=0;
				}
			}
			
			br.close();
		}catch(Exception e){}
		return pop;
	}

	public static ArrayList<String[]> STR11(String[][] inputDataTEC, int num,int count, double stopPP, double stoplose ) {
		// TODO Auto-generated method stub
		ArrayList<String[]> a=new ArrayList<String[]>();
		ArrayList<String[]> b=new ArrayList<String[]>();
		ArrayList<String[]> c=new ArrayList<String[]>();
		for(int i=0;i<num-1;i++){
			String aa[]=new String[4];
			String s = String.valueOf(i);
			if(!inputDataTEC[i][count].equals("")){
				aa[0]=s;//編號
				aa[1]=inputDataTEC[i][0];//日期
				aa[2]=inputDataTEC[i][count];//buy or sell
				aa[3]=inputDataTEC[i+1][1];//隔天的OPEN PRICE
				a.add(aa);
			}
		}
		
		for(int j=0;j<a.size();j++){//meet first 1
			String st[]=a.get(j);
			if(st[2].equals("1")){
				b.add(st);
				break;
			}
			if(st[2].equals("10")){
				st[2]="1";
				b.add(st);
				break;
			}
		}
		if(b.size()==0){
			return b;
		}
		else{
			int bi=0;
			for(int j=0;j<a.size();j++){
				String st[]=a.get(j);
				String st1[]=b.get(bi);
				int n=Integer.parseInt(st[0]);
				int n1=Integer.parseInt(st1[0]);
				double P=Double.parseDouble(st[3]);
				double P1=Double.parseDouble(st1[3]);
				if(n>n1){//第一個1以前的0不管
					if(!st1[2].equals(st[2])){
						if(st[2].equals("10")){
							if(st1[2].equals("1")&&(((P-P1)/P1)>stopPP||((P-P1)/P1)<stoplose)){
								st[2]="0";
								b.add(st);
								bi++;
							}
							else if(st1[2].equals("0")){
								st[2]="1";
								b.add(st);
								bi++;
							}
						}
						else if(st[2].equals("0")){
							if(((P-P1)/P1)>stopPP||((P-P1)/P1)<stoplose){
								b.add(st);
								bi++;
							}
						}
						else{
							b.add(st);
							bi++;
						}
					}
				}
			}
		}

		String ss[]=b.get(b.size()-1);
		if(ss[2].equals("1")){//最後一個是買的話
			for(int i=0;i<b.size()-1;i++){
				String st[]=b.get(i);
				c.add(st);
			}
			for(int i=0;i<c.size();i++){
				String st[]=c.get(i);
				for(int u=0;u<st.length;u++){
					//System.out.print(st[u]+"　");
				}//System.out.println();
			}
			return c;
		}
		else{
			for(int i=0;i<b.size();i++){
				String st[]=b.get(i);
				for(int u=0;u<st.length;u++){
					//System.out.print(st[u]+"　");
				}//System.out.println();
			}
			return b;
		}
	}

	public static ArrayList<String[]> STR(String[][] inputDataTEC, int num,int count) {
		// TODO Auto-generated method stub
		ArrayList<String[]> a=new ArrayList<String[]>();
		ArrayList<String[]> b=new ArrayList<String[]>();
		ArrayList<String[]> c=new ArrayList<String[]>();
		for(int i=0;i<num-1;i++){
			String aa[]=new String[4];
			String s = String.valueOf(i);
			//System.out.println(count+","+i);
			if(!inputDataTEC[i][count].equals("")){
				aa[0]=s;
				aa[1]=inputDataTEC[i][0];
				aa[2]=inputDataTEC[i][count];
				aa[3]=inputDataTEC[i+1][1];//隔天的OPEN PRICE
				a.add(aa);
			}
		}

		for(int j=0;j<a.size();j++){//meet first 1
			String st[]=a.get(j);
			if(st[2].equals("1")){
				b.add(st);
				break;
			}
			if(st[2].equals("10")){
				st[2]="1";
				b.add(st);
				break;
			}
		}
	/*	for(int i=0;i<b.size();i++){
			String st[]=b.get(i);
			for(int u=0;u<st.length;u++){
				System.out.print(st[u]+"　");
			}System.out.println();
		}*/
		if(b.size()==0){
			return b;
		}
		
		else{
			int bi=0;
			for(int j=0;j<a.size();j++){
				String st[]=a.get(j);
				String st1[]=b.get(bi);
				int n=Integer.parseInt(st[0]);
				int n1=Integer.parseInt(st1[0]);
				if(n>n1){
					if(!st1[2].equals(st[2])){
						if(st[2].equals("10")){
							if(st1[2].equals("1")){
								st[2]="0";
								b.add(st);
								bi++;
							}
							else if(st1[2].equals("0")){
								st[2]="1";
								b.add(st);
								bi++;
							}
						}
						else if(st[2].equals("1")){
							b.add(st);
							bi++;
						}
						else{
							b.add(st);
							bi++;
						}
					}
					//System.out.print(st[i]+" ");
				}
			}
		}
		
		//b.remove(b.size()-1);
		String ss[]=b.get(b.size()-1);
		if(ss[2].equals("1")){
			for(int i=0;i<b.size()-1;i++){
				String st[]=b.get(i);
				c.add(st);
			}
			return c;
		}
		else{
			return b;
		}
	}
	
	public static int count(ArrayList<String[]> ma) {
		// TODO Auto-generated method stub
		int count=0;
		for(int i=0;i<ma.size();i++){
			String st[]=ma.get(i);
			if(st[2].equals("0"))
				count++;
			}
		return count;
	}
	
	public static double mareturnrate(ArrayList<String[]> mA) {
		// TODO Auto-generated method stub
		double sum=0;
		double n1=0;
		int coo=0;
		for(int i=1;i<mA.size();i+=2){
			String st[]=mA.get(i);
			String st1[]=mA.get(coo);
			double co=Double.parseDouble(st[3]);
			double co1=Double.parseDouble(st1[3]);
			if(i%2==1){
				n1=(co-co1)/co1;
			}
			coo+=2;
			sum=sum+n1;
		}
		return sum/(mA.size()/2);
	}

	public static double mareturnrate1(ArrayList<String[]> mA) {
		// TODO Auto-generated method stub
		double sum=0;
		double n1=0; 
		int coo=0;
		for(int i=1;i<mA.size();i+=2){
			String st[]=mA.get(i);
			String st1[]=mA.get(coo);
			double co=Double.parseDouble(st[3]);
			double co1=Double.parseDouble(st1[3]);
			if(i%2==1){
				n1=(co-co1-(co1*0.001425)-(co*0.001425)-(co*0.003))/co1;
			}
			coo+=2;
			sum=sum+n1;
		}
		 return sum/(mA.size()/2);
	}


	public static double MDD(ArrayList<String[]> mA,int count) {
		// TODO Auto-generated method stub
		
		double n1=0;
		double re[]=new double[count];
		int coo=0;
		int j=0;
		for(int i=1;i<mA.size();i+=2){
			String st[]=mA.get(i);
			String st1[]=mA.get(coo);
			double co=Double.parseDouble(st[3]);
			double co1=Double.parseDouble(st1[3]);
			if(i%2==1){
				n1=(co-co1)/co1;
				re[j]=n1;
				j++;
			}
			coo+=2;
		}
		double Min=9999;

		for(int i=0;i<count;i++){
			if(re[i]<Min)
				Min=re[i];
		}
	//	System.out.println("PP"+Min);
		return Math.pow(Min,1);
	}

	public static double MDD1(ArrayList<String[]> mA,int count) {
		// TODO Auto-generated method stub
		
		double n1=0;
		double re[]=new double[count];
		int coo=0;
		int j=0;
		for(int i=1;i<mA.size();i+=2){
			String st[]=mA.get(i);
			String st1[]=mA.get(coo);
			double co=Double.parseDouble(st[3]);
			double co1=Double.parseDouble(st1[3]);
			if(i%2==1){
				n1=(co-co1-(co1*0.001425)-(co*0.001425)-(co*0.003))/co1;
				re[j]=n1;
				j++;
			}
			coo+=2;
		}
		double Min=9999;
		for(int i=0;i<count;i++){
			if(re[i]<Min)
				Min=re[i];
		}
		return Math.pow(Min,1);
	}
	
	private static ArrayList<Integer> RReturnRate(double[] RankReturnRate, double[] Rank1ReturnRate,int chooseReturnRate, ArrayList<Integer> alre) {
		// TODO Auto-generated method stub
	//	ArrayList<Integer> alre=new ArrayList<>();
		int coo1=0;
		for (int i =0; i <RankReturnRate.length ; i++){	
			if(RankReturnRate[i]>RankReturnRate[chooseReturnRate]){
				coo1++;
			}
		}
	//	System.out.println("5---NK"+coo1);
		if(coo1<chooseReturnRate){
			int x=0;
			//System.out.println(x);
			for (int i = 0; i <RankReturnRate.length; i++){
					if(RankReturnRate[i]==RankReturnRate[chooseReturnRate-1]){
					x++;
				}
			}
		//System.out.println(x);
			
			List<Integer> al=new ArrayList<>();
			while(al.size()<chooseReturnRate-coo1){
				int j=(int) ((Math.random()*x)+coo1);
				if(al.contains(j)) 
						continue;     //重複的不加入
				else
					al.add(j);
					
			}
			for(int j=0;j<coo1;j++){
				alre.add((int) Rank1ReturnRate[j]);
			}
			for(int j=0;j<al.size();j++){
				int a=al.get(j);
				alre.add((int) Rank1ReturnRate[a]);
			}
		}
		if(coo1==chooseReturnRate){
			for (int i = 0;  i < chooseReturnRate; i++){
				alre.add((int) Rank1ReturnRate[i]);
			}
		}
		return alre;
	}
	
	private static ArrayList<Integer> RReturnRate1(double[] rankbcount, double[] rank1bcount, int choosecount, ArrayList<Integer> alre) {
		// TODO Auto-generated method stub
		int coo1=0;
		for (int i =0; i <rankbcount.length ; i++){	
			if(rankbcount[i]<rankbcount[choosecount]){
				coo1++;
			}
		}
	//	System.out.println("555NK"+coo1);
		if(coo1<choosecount){
			int x=0;
			for (int i = 0; i <rankbcount.length; i++){
					if(rankbcount[i]==rankbcount[choosecount-1]){
					x++;
				}
			}
		//	System.out.println("555NK"+x);
			List<Integer> al=new ArrayList<>();
			while(al.size()<choosecount-coo1){
				int j=(int) ((Math.random()*x)+coo1);
				if(al.contains(j))
					continue;     //重複的不加入
				else
					al.add(j);
			}
			for(int j=0;j<coo1;j++){
				alre.add((int) rank1bcount[j]);
			}
			for(int j=0;j<al.size();j++){
				int a=al.get(j);
				alre.add((int) rank1bcount[a]);
			}
		}

		

  

		

	  if(coo1==choosecount){

		for (int i = 0;  i < choosecount; i++){

			// System.out.println("5RANK"+Rank[i]); 

		 alre.add((int) rank1bcount[i]);

		}

	  }

		return alre;

	}
	
	private static Hashtable<String, chromosome> calculateFitnessValue(Hashtable<String, chromosome> population,

			Hashtable<String, Hashtable> input, int maxCaptial,double stoppp,double stoplose) {
		// TODO Auto-generated method stub
		for(int i=0; i<population.size();i++){
			//calculate portfolio satisfaction of each chromosome
			Hashtable  ht = population.get(""+i).groupPart;
			String[][] st = new String[ht.size()][];
			
			for(int j=0; j<ht.size(); j++){
			//	System.out.println("sssA="+population.get(""+i).groupPart.get(""+j));
				st[j] = population.get(""+i).groupPart.get(""+j).toString().split(",");
			}
		
			//1. Find all stock portfolio combinations
			ArrayList<String> possibleStockCombination = new ArrayList<String>();
			possibleStockCombination = getCombination(st, ht.size());//目前只有K=3,4,5,6 結果會正確
			double roi=0;
			double risk=0;
			double suitability=0;
			double subPS =0;
			double subPS1 =0;
			double risktr=0;

			String stopp=stoppp+","+stoplose;
			Hashtable s2 = input.get(""+stopp);
			double[][] inputData=(double[][]) s2.get("0");
			Factor factor = new Factor();
			double MDD[] = Factor.varArray(inputData);
			for(int u=0;u<MDD.length;u++){
				System.out.println("///"+u+""+MDD[u]);
			}

			for(int hh=0;hh<inputData.length;hh++){
				for(int j=0;j<inputData[0].length;j++){
					System.out.print(inputData[hh][j]+" , ");
				} System.out.println();
			}

			for(int j=0; j<possibleStockCombination.size(); j++){
				String[] stockCombi = possibleStockCombination.get(j).split(",");
				roi = ROI(population.get(""+i).strategyweight, inputData,stockCombi, maxCaptial);
				risk = RISK(stockCombi, MDD);
				subPS+=roi;
				subPS1+=risk;
			}
			double subPS11=subPS1/possibleStockCombination.size();

			population.get(""+i).fitness[1] =subPS/possibleStockCombination.size();//roi
			population.get(""+i).fitness[2] = balanceFactor(population.get(""+i).groupPart);
			population.get(""+i).fitness[3] = subPS11;//risk
			population.get(""+i).fitness[4] = balanceWeight(population.get(""+i).strategyweight);
			population.get(""+i).fitness[0] = Math.pow(population.get(""+i).fitness[1],1)* Math.pow(population.get(""+i).fitness[2],2)*Math.pow(population.get(""+i).fitness[3],1)*Math.pow(population.get(""+i).fitness[4],1);

			System.out.println("F"+population.get(""+i).fitness[0]);
		}
		return population;
	}
	private static ArrayList<String> getCombination(String[][] st, int size) {
		ArrayList<String> combineString = new ArrayList<String>();
		//此法只能限制K=6的時候使用
		if(size==6){
			for(int j=0; j<st[0].length; j++){
				String st1 = st[0][j];
				for(int k=0; k<st[1].length; k++){
					String temp1=st1;
					st1 += ","+st[1][k];
					for(int l=0; l<st[2].length; l++){
						String temp2=st1;
						st1 += ","+st[2][l];
						for(int m=0; m<st[3].length; m++){
							String temp3=st1;
							st1 += ","+st[3][m];	
							for(int n=0; n<st[4].length; n++){
								String temp4 = st1;
								st1 += ","+st[4][n];
								for(int o=0; o<st[5].length; o++){
									String temp5 = st1;
									st1 += ","+st[5][o];
									combineString.add(st1);
									st1 = temp5;
								}
								st1 = temp4;
							}
							st1 = temp3;
						}
						st1=temp2;
					}
					st1=temp1;
				}
				
			}
		}
		//此法只能限制K=5的時候使用
		if(size==5){
			for(int j=0; j<st[0].length; j++){
				String st1 = st[0][j];
				for(int k=0; k<st[1].length; k++){
					String temp1=st1;
					st1 += ","+st[1][k];
					for(int l=0; l<st[2].length; l++){
						String temp2=st1;
						st1 += ","+st[2][l];
						for(int m=0; m<st[3].length; m++){
							String temp3=st1;
							st1 += ","+st[3][m];
							for(int n=0; n<st[4].length; n++){
								String temp4 = st1;
								st1 += ","+st[4][n];
								combineString.add(st1);
								st1 = temp4;
							}
							st1 = temp3;
						}
						st1=temp2;
					}
					st1=temp1;
				}
			}
		}

		//此法只能限制K=4的時候使用
		if(size==4){
			for(int j=0; j<st[0].length; j++){
				String st1 = st[0][j];
				for(int k=0; k<st[1].length; k++){
					String temp1=st1;
					st1 += ","+st[1][k];
					for(int l=0; l<st[2].length; l++){
						String temp2=st1;
						st1 += ","+st[2][l];
						for(int m=0; m<st[3].length; m++){
							String temp3 = st1;
							st1 += ","+st[3][m];
							combineString.add(st1);
							st1 = temp3;
						}
						st1=temp2;
					}
					st1=temp1;
				}
				
			}
		}
				
				//此法只能限制K=3的時候使用
		if(size==3){
			for(int j=0; j<st[0].length; j++){
				String st1 = st[0][j];
				for(int k=0; k<st[1].length; k++){
					String temp1=st1;
					st1 += ","+st[1][k];
					for(int l=0; l<st[2].length; l++){
						String temp2 = st1;
						st1 += ","+st[2][l];
						combineString.add(st1);
						st1=temp2;
					}
					st1=temp1;
				}
				
			}
		}
		
		return combineString;
	}
	
	private static double ROI(ArrayList strategyweight, double[][] inputData, String[] StockCombination, int maxCaptial) {
			double roi=0;
		
			for(int j=2; j<strategyweight.size(); j++ ){
				int stockNum = Integer.parseInt(StockCombination[j-2]);
			//	System.out.print("stockNum"+stockNum);
				double a = inputData[stockNum][2];//Return rate
				
				double c = Double.parseDouble(strategyweight.get(j).toString());//權重
				double d = a*c*maxCaptial;//Return*權重
				roi =roi+d;
		//	System.out.print(" a ="+ a +" b ="+ b +" c ="+ c +" d ="+ d+" ROI="+((b-a)*(c)+d*(c)));
		//		System.out.print("stockNum"+stockNum+" a ="+ a +" c ="+ c +" d ="+ d +" ROI="+roi);
			}
		return roi;
	}
	
	private static double RISK(String[] StockCombination, double[] mDD) {
		double min=999999999; 
		double MDD=0;
		for(int j=0; j<StockCombination.length; j++ ){
			int stockNum = Integer.parseInt(StockCombination[j]);
			MDD = mDD[stockNum];//MDD
			if(MDD<min){
				min=MDD;
			}
		}
		return min;
	}
	
	static double balanceFactor(Hashtable groupPart) {
		    double balabce = 0;
		    double N = 0;
		    for(int i=0; i<groupPart.size(); i++)
		    	N += groupPart.get(""+i).toString().split(",").length;
			
		    for(int i=0; i<groupPart.size(); i++){
		    	String[] st = groupPart.get(""+i).toString().split(",");
		    	balabce = balabce - (st.length/N)*Math.log(st.length/N);
		    }
		return balabce*balabce;
	}


	private static double balanceWeight(ArrayList strategyweight) {
		// TODO Auto-generated method stub
		double balabce = 0;
		double N = 100;
		String we=  (String) strategyweight.get(0).toString();
		String st[]= we.split("0");
		for(int i=0; i<st.length; i++){
			String[] stl=st[i].split("");
			balabce = balabce - (stl.length/N)*Math.log(stl.length/N);
		}
		return balabce*balabce;
	}

	private static void writeExperimentValuetoFile(Hashtable<String, chromosome> population, BufferedWriter br, int GeneNum, long Time)throws IOException {
		   //計算平均值
		   double sumFitness = 0, sumreturn= 0, sumBallance = 0,  sumrisk = 0, sumWB = 0;
		   int pSize = population.size();
		   for(int i=0; i<population.size(); i++){
				sumFitness += population.get(""+i).fitness[0];//Fitness
				sumreturn += population.get(""+i).fitness[1];//return
				sumBallance += population.get(""+i).fitness[2];//group balance
				sumrisk += population.get(""+i).fitness[3];//risk
				sumWB += population.get(""+i).fitness[4];//Weight balance
			   /*sumDiss += population.get(""+i).fitness[5];*/
		   } 
		   
		   //輸出至檔案
		   //1.加新參數
		   br.write(GeneNum + " "+ sumFitness + " "+ sumreturn + " "+ sumBallance+" "+sumrisk+" "+sumWB+" "+Time);
		   //2.沒加任何參數 (最原始的)
//			   br.write(GeneNum + " "+ (sumFitness/pSize) + " "+ (sumPortfolioSatisfy/pSize) + " "+ (sumBallance/pSize)+" "+Time);
		   br.newLine();
			
		}
		
	static Hashtable<String, chromosome> executeSelectionOperator(Hashtable<String, chromosome> chro, int pSize){
		//開始以菁英選擇法複製chromosome
		Hashtable<String, chromosome> afterSelection = new Hashtable<String, chromosome>();
		for(int i=0; i<pSize; i++){
			afterSelection.put(""+i, findMaxFitness(chro));
		}
		return afterSelection;
	}
		
		
	static chromosome findMaxFitness(Hashtable<String, chromosome> chro){
		chromosome chroWithMaxFit = new chromosome();
		int maxIndex = 0;
		double maxFitValue=-10000000;

		for(Enumeration e = chro.keys(); e.hasMoreElements();){
			String num = (String)e.nextElement();
		//	System.out.println("num="+num);
			//System.out.println("chro.get(num).fitness[0]="+chro.get(num).fitness[0]);
			if(chro.get(num).fitness[0]>maxFitValue){
				maxFitValue = chro.get(num).fitness[0];
			//	System.out.println("a="+chro.get(num).fitness[0]+ " b="+maxFitValue + "num="+num);
				maxIndex=Integer.parseInt(num);
			//	System.out.println("maxIndexINside="+maxIndex);
			}
		}
		chroWithMaxFit = copyOneChromosome(chro.get(""+maxIndex));
		chro.remove(""+maxIndex);
		return chroWithMaxFit;
	}
		
	static Hashtable<String, chromosome> executeCrossoverOperator(Hashtable<String, chromosome> population, double cRate,int K) {
		
		int pupSize = population.size();
		//計算應做交配的染色體個數
		int CrossoverQuantity=(int)(pupSize*cRate);
		if(CrossoverQuantity%2!=0) CrossoverQuantity=CrossoverQuantity-1;
		//System.out.println("totalCrossoverQuantity="+totalCrossoverQuantity);


		//找出不重複的交配染色體
		int crossoverCNumber[]=new int[CrossoverQuantity];
		for(int i=0; i<CrossoverQuantity; i++)	{
			crossoverCNumber[i]=(int)(Math.random()*pupSize);
			for(int j=0; j<i; j++){
				if(crossoverCNumber[j]==crossoverCNumber[i]) i--;
			}
		}

		int currentNum = pupSize;
		for(int i=0; i<CrossoverQuantity; i+=2){
//				//for write example
//				if(i==0){//Print做crossover的第一組兩個染色體
//					System.out.println("\ncrossover:");
//					for(int k=i; k<=i+1; k++){
//						for(int j=0; j<population.get(""+i).groupPart.size(); j++)
//							System.out.print(population.get(""+crossoverCNumber[k]).groupPart.get(""+j).toString()+" ");
//						for(int j=0; j<population.get(""+i).strategyweight.size(); j++)
//							System.out.print(population.get(""+crossoverCNumber[k]).strategyweight.get(j).toString()+" ");
//						System.out.println();
//					}
//				}
			
			//針對stock portfolio part作交配
			chromosome[] temp;
			temp = onePointCO_strategyweight(population.get(""+crossoverCNumber[i]), population.get(""+crossoverCNumber[i+1]),K);
			//for write example
			//if(i==0){//Print做crossover的第一組兩個染色體
//					System.out.println("After portfolio part crossover:");
//				for(int k=0; k<=1; k++){
//						for(int j=0; j<population.get(""+i).groupPart.size(); j++)
//							System.out.print(temp[k].groupPart.get(""+j).toString()+" ");
//							for(int j=0; j<population.get(""+i).strategyweight.size(); j++)
//							System.out.print(temp[k].strategyweight.get(j).toString()+" ");
//						System.out.println();
//					}
//				}
			
			//針對grouping part作交配
			temp = crossover_GroupingPart(temp);
			//for write example
//				if(i==0){//Print做crossover的第一組兩個染色體
//					System.out.println("new chromosome:"+(i/2+1));
//					System.out.println("After group part crossover:");
//					for(int k=0; k<=1; k++){
//						for(int j=0; j<population.get(""+i).groupPart.size(); j++)
//							System.out.print(temp[k].groupPart.get(""+j).toString()+" ");
//						for(int j=0; j<population.get(""+i).stockPortfolio.size(); j++)
//							System.out.print(temp[k].stockPortfolio.get(j).toString()+" ");
//						System.out.println();
//					}
//					System.out.println();
//				}
			
			//System.out.println("grouping part作交配");
			for(int j=0; j<temp.length; j++)
				population.put(""+(currentNum++), temp[j]);
		
		}
		return population;
	}
	static chromosome[] crossover_GroupingPart(chromosome[] chro) {
//			for(int i=0;i<chro[0].groupPart.size();i++)
//				System.out.println("chro[0]_Group"+i+": "+chro[0].groupPart.get(""+i).toString());
//			for(int i=0;i<chro[1].groupPart.size();i++)
//				System.out.println("chro[1]_Group"+i+": "+chro[1].groupPart.get(""+i).toString());

		//複製base chromosome
		chromosome chroBase = copyOneChromosome(chro[0]);
		//Base chromosome, 選出插入起點
		int indexBase = (int)(chro[0].groupPart.size()*Math.random());
		//inserted chromosome, 選出切割起點與終點
		int indexCutSequenceStart;
		int indexSequenceEnd;
		
		do{
			indexCutSequenceStart = (int)(chro[1].groupPart.size()*Math.random());
			indexSequenceEnd = (int)(chro[1].groupPart.size()*Math.random());
				
		}while(indexCutSequenceStart>=indexSequenceEnd);
		//System.out.println("PP");
		//從inserted chromosome取出必需插入base chromosome的群組
		Hashtable ht = new Hashtable();
		int a = 0;
		for(int i=indexCutSequenceStart; i<indexSequenceEnd; i++){
			ht.put(""+a, chro[1].groupPart.get(""+i));
			a++;
		}
		
//			for(int i=0; i<ht.size(); i++){
//				System.out.println("Ht="+ht.get(""+i).toString());
//			}
		
//			for(int i=0; i<chro[0].groupPart.size(); i++){
//				System.out.println("ChroBefo="+chroBase.groupPart.get(""+i).toString());
//				System.out.println("ChroBefo0="+chro[0].groupPart.get(""+i).toString());
//			}
		
		
		/*for(int i=0; i<chro[1].groupPart.size(); i++){
			//System.out.println("ChroBefo="+chroBase.groupPart.get(""+i).toString());
			System.out.println("ChroBefo1="+chro[1].groupPart.get(""+i).toString());
			
			
		}*/
		
	//bug-------------------------------------------------------------------
		//根據欲加入的group的股票, 將base chromosome有包含的股票從刪除
//		    for(Enumeration e = ht.keys();e.hasMoreElements();){
//		    	String st = e.nextElement().toString();
//		    	String[] stArray=ht.get(st).toString().split(",");
//		    	
//		    	for(int i=0; i<chroBase.groupPart.size();i++){
//		    		String baseSt = chroBase.groupPart.get(""+i).toString();
//		    		for(int j=0; j<stArray.length; j++){
//		    			if(baseSt.contains(stArray[j]))
//		    				baseSt=baseSt.replace(stArray[j]+",", "");
//		    			
//		    		}
//		    		chroBase.groupPart.put(""+i, baseSt);
//		    	}
//		    }
		
		//Debug  假如stArray[j]=0 ;預期 0,10,=>10,而不是 1, 
		for(Enumeration e = ht.keys();e.hasMoreElements();){
			String st = e.nextElement().toString();
			String[] stArray=ht.get(st).toString().split(",");
			
			for(int i=0; i<chroBase.groupPart.size();i++){
				String baseString="";
				String[] baseSt = chroBase.groupPart.get(""+i).toString().split(",");
				for(int j=0; j<stArray.length; j++){
					for(int k=0; k<baseSt.length; k++)
						if(baseSt[k].equals(stArray[j]))
							baseSt[k] = baseSt[k].replace(stArray[j], "");
				} 
				for(int j=0; j<baseSt.length; j++){
					if(!baseSt[j].isEmpty())
						baseString += baseSt[j]+","; 
				}
				chroBase.groupPart.put(""+i, baseString);
			}
		}
		//System.out.println("QQ");
		ArrayList aList = new ArrayList();
		int count=0;
		for(int i=0; i<indexBase; i++){
			String st = chroBase.groupPart.get(""+i).toString();
			if(st.length()!=0){
				aList.add(count, st);
				count++;
				//System.out.println("got it1");
			}
			
		}
		for(int i=0; i<ht.size(); i++){
			String st = ht.get(""+i).toString();
			aList.add(count, st);
			count++;
		}
		for(int i=indexBase; i<chroBase.groupPart.size(); i++){
			String st = chroBase.groupPart.get(""+i).toString();
			if(st.length()!=0){
				aList.add(count, st);
				count++;
				//System.out.println("got it2");
			}
		}
//		    System.out.println("ArrayList="+aList);
//		    System.out.println("AA");
		
		if(aList.size()>chro[0].groupPart.size()){
			int removalNumGroup = aList.size() - chro[0].groupPart.size();
			for(int i=0; i<removalNumGroup;i++){
				aList = adjustNumberofGroup(aList, -1);//-1表示要減少group數目
				//System.out.println("減少group數目");
			}
		}
		
		if(aList.size()<chro[0].groupPart.size()){
			int addNumGroup =  chro[0].groupPart.size() - aList.size();
			for(int i=0; i<addNumGroup;i++){
				aList = adjustNumberofGroup(aList, 1);//1表示要增加group數目
				//System.out.println("增加group數目");
			}     
		
		}
		
//		    System.out.println("ArrayList_After="+aList);
		
		for(int i=0; i<aList.size(); i++)
			chro[1].groupPart.put(""+i, aList.get(i));   
//			for(int i=0;i<chro[1].groupPart.size();i++)
//				System.out.println("chro[1]_Group"+i+": "+chro[1].groupPart.get(""+i).toString());
		return chro;
	}
		
	static chromosome copyOneChromosome(chromosome chro) {
		chromosome copiedChro= new chromosome(); 
		
		//複製group part
		Hashtable ht = new Hashtable();
		for(int i=0; i<chro.groupPart.size(); i++)
			ht.put(""+i, chro.groupPart.get(""+i));
		
		//複製ftiness value
		double[] fit = new double[chro.fitness.length];
		for(int i=0; i<fit.length; i++)
			fit[i] = chro.fitness[i];
				
		//複製stock portfolio
		ArrayList strategyweight = new ArrayList();
		for(int i=0; i<chro.strategyweight.size(); i++)
			strategyweight.add(i, chro.strategyweight.get(i));
				
		copiedChro.groupPart = ht;
		copiedChro.fitness = fit;
		copiedChro.strategyweight = strategyweight;
		
		return copiedChro;
	}
	private static ArrayList adjustNumberofGroup(ArrayList aList, int i) {
		ArrayList newAList = new ArrayList();
		if(i==-1){
			//find group with minimum element
			int groupNumwithMinElement = 100;
			int index=0;
			for(int j=0; j<aList.size(); j++){
				//int a = (aList.get(j).toString().split(",").length);
				//System.out.println("a="+a);
				if((aList.get(j).toString().split(",").length)<groupNumwithMinElement){
					groupNumwithMinElement = aList.get(j).toString().split(",").length;	
					index = j;
				}
			}
			//System.out.println("index="+index);
			//System.out.println("aList.get("+index+")="+aList.get(index).toString());
			int randomNum;
			do{
				randomNum = (int)(Math.random()*aList.size());
			}while(randomNum==index);
			
			//System.out.println("Before="+aList);
			//System.out.println("randomNum="+randomNum);
			
			String addString = aList.get(randomNum)+""+aList.get(index);
			//System.out.println("addString="+addString);
		
			for(int j=0; j<aList.size(); j++){
				if(j==index){
					
				}else if(j==randomNum){
					newAList.add(addString );
				}else{
					newAList.add(aList.get(j) );
					
				}
			}
			
			//System.out.println("After="+newAList);
			
				
		}
		
		if(i==1){
			//find group with maximum element
			int groupNumwithMaxElement = 0;
			int index=0;
			for(int j=0; j<aList.size(); j++){
				if(aList.get(j).toString().split(",").length>groupNumwithMaxElement){
					groupNumwithMaxElement =aList.get(j).toString().split(",").length;
					index = j;
				}
			}
			
			String[] splitStringArray = aList.get(index).toString().split(",");
			String st1 = "", st2="";
			for(int j=0;j<splitStringArray.length/2; j++) st1 = st1+splitStringArray[j]+",";
			for(int j=splitStringArray.length/2;j<splitStringArray.length; j++) st2 = st2+splitStringArray[j]+",";
//				System.out.println("Before="+aList);
			
			
			for(int j=0; j<aList.size(); j++){
				if(j==index){
					newAList.add(st1 );
					newAList.add(st2 );
				}else{
					newAList.add(aList.get(j) );
				}
			}
			
//				System.out.println("After="+newAList);
			
			
			
		}
		
		return newAList;
		
	}

	static chromosome[] onePointCO_strategyweight(chromosome chro1, chromosome chro2,int K) {
		chromosome[] crossoverChro = new chromosome[2];
		crossoverChro[0] = copyOneChromosome(chro1);
		crossoverChro[1] = copyOneChromosome(chro2);
		
//			for(int i=0; i<chro1.groupPart.size(); i++){
//				//System.out.println("ChroBefo="+chroBase.groupPart.get(""+i).toString());
//				System.out.println("ChroBefoSP0="+chro1.groupPart.get(""+i).toString());
//				
//				
//			}
		
//			for(int i=0; i<chro2.groupPart.size(); i++){
//				//System.out.println("ChroBefo="+chroBase.groupPart.get(""+i).toString());
//				System.out.println("ChroBefoSP1="+chro2.groupPart.get(""+i).toString());
	//
//			}
		
		
		//決定stockPortfolio part的切割點
		int cutPoint=0;
		int cutPoint1=0;
		int excutpoint=0;
		do{
			cutPoint = (int)(Math.random()*(K+100));
		}while(cutPoint==(K+100)-1);
		
		do{
			cutPoint1 = (int)(Math.random()*(K+100));
		}while((cutPoint==0 &&cutPoint1==(K+100)-1)||cutPoint==cutPoint1);
	   
		if (cutPoint>cutPoint1){
			excutpoint=cutPoint;
			cutPoint=cutPoint1;
			cutPoint1=excutpoint;
		}	
	 //   System.out.println("crossoverChro[0].stockPortfolioSize="+cutPoint+" "+cutPoint1);
	   //根據cutpoint交換c1與c2的strategyweight part
		String first= crossoverChro[0].strategyweight.get(0).toString();
		String second= crossoverChro[1].strategyweight.get(0).toString();
		String fir[]=first.split("");
		String sec[]=second.split("");

		ArrayList a1 = new ArrayList();
		ArrayList a2 = new ArrayList();
		
	   int a = fir.length;
	   String weight1[]=new String[a];
	   String weight2[]=new String[a];
	   int count=0;
	   int count1=0;
	   String one="0";
	   
	   while(true){ 
			if(cutPoint1==cutPoint){
				do{
					cutPoint = (int)(Math.random()*(K+100));
				}while(cutPoint==(K+100)-1);
				
				do{
					cutPoint1 = (int)(Math.random()*(K+100));
				}while((cutPoint==0 &&cutPoint1==(K+100)-1)||cutPoint==cutPoint1);
			   
				if (cutPoint>cutPoint1){
					excutpoint=cutPoint;
					cutPoint=cutPoint1;
					cutPoint1=excutpoint;
				}	
			}    
			
			for(int i=cutPoint; i<=cutPoint1; i++){
				
						if(fir[i].equals("1")){
							count++;
						}
						if(sec[i].equals("1")){
							count1++;
						}
			}
			
			if(count==count1) break;
					
					cutPoint1--;
					count=0;
					count1=0;
			
			
	   }

		for(int i=0; i<a; i++){
			if(i<cutPoint||i>cutPoint1){
				weight1[i]=fir[i];
				weight2[i]=sec[i];
			}else{
				weight1[i]=sec[i];
				weight2[i]=fir[i];
			}
		}
		
		String weight="";
		String weight0="";
		for(int i=0; i<a; i++){
			 weight= weight+weight1[i];
		}
	 
		for(int i=0; i<a; i++){
			weight0= weight0+weight2[i];;
		}
	   // System.out.print(weight);
	 //   System.out.println();
	   
		
		String[] aa=weight.split("0");
		String[] aa1=weight0.split("0");
	  //  System.out.print(aa1[0].length());
		
		double COO=0;
		double COO1=0;
		double[] CO=new double[K+1];
		double[] CO1=new double[K+1];
		for(int o=0;o<aa.length;o++){
				COO=(aa[o].length());
				CO[o]=COO;
		}
		
		for(int o=0;o<aa1.length;o++){
			COO1=(aa1[o].length());
			CO1[o]=COO1;
		}

		a1.add((String)weight+"");
		a2.add((String)weight0+"");
		for(int u=0;u<K+1;u++){
			a1.add((((100/(a-K))*CO[u])/100)+"");	 
			a2.add((((100/(a-K))*CO1[u])/100)+"");	
		}
		crossoverChro[0].strategyweight = a1;
		crossoverChro[1].strategyweight = a2;
		
		return crossoverChro;
	}
		
	static Hashtable<String, chromosome> executeMutationOperator(Hashtable<String, chromosome> population, double mutationRate, int pSize, int K) {
		//mutation on stock portfolio part
		
		String oo=(String) population.get(""+0).strategyweight.get(0);
	//	System.out.println("After="+oo.length());
		
		int mutatioGene = (int)(oo.length()*pSize*mutationRate);
		Hashtable mutationPositionHS = new Hashtable();
		Hashtable mutationPositionHS1 = new Hashtable();
		int currentPupulationSize = population.size(); 
		
		for(int i=0; i<mutatioGene; i++){
			
			int mutationPoint=0;
			int mutationPoint1=0;
			mutationPoint = (int)((K+100)*pSize*Math.random());
			
			do{
			mutationPoint1 = (int)(oo.length()*pSize*Math.random());
			}while(mutationPoint==mutationPoint1);
			
			
			
			if(!mutationPositionHS.containsKey(""+mutationPoint)&&!mutationPositionHS1.containsKey(""+mutationPoint1)){
				mutationPositionHS.put(""+mutationPoint, "");
				mutationPositionHS1.put(""+mutationPoint1, "");
				int whichChro = mutationPoint/(int)(oo.length());
				int whichPosition = mutationPoint%(int)(oo.length());
				int whichPosition1= mutationPoint1%(int)(oo.length());
			//	System.out.println("firstwhichPosition1 "+whichPosition1+" "+whichPosition);	
				chromosome chro =  copyOneChromosome(population.get(""+whichChro));
				ArrayList aL = new ArrayList();
				//mutation on strategyweight
					String weight = chro.strategyweight.get(0).toString();
					String mu[]=weight.split("");
					String one="1";
					String zero="0";
					String Finweight="";
					//System.out.println("K"+oo.length());
					while((mu[whichPosition]+"").equals(mu[whichPosition1]+"")||(whichPosition1==whichPosition)){
						whichPosition1 = (int)(oo.length()*Math.random());
					}
				for(int j=0; j<mu.length; j++){
					if(j==whichPosition||j==whichPosition1){
						if((mu[j]+"").equals(one))
							Finweight=Finweight+zero;
						else
							Finweight=Finweight+one;
					}else{
						Finweight=Finweight+mu[j];
					}
				}
				String[] aa=Finweight.split("0");
				int CO1=0;
				double[] CO=new double[K+1];
				for(int o=0;o<aa.length;o++){
						 CO1=(aa[o].length());
						 CO[o]=CO1;
					  }
				aL.add(Finweight);
				for(int u=0;u<K+1;u++){
					aL.add((((100/(oo.length()-K))*CO[u])/100+""));	 
				}

				chro.strategyweight = aL; //把aL值存回chro
				population.put(""+currentPupulationSize, chro);
				currentPupulationSize++;
			}
			else i--;
		}

		//mutation on group part
		chromosome chro;
		int mutatioGeneOnStockPart = (int)(K*pSize*mutationRate);
		Hashtable mutationPositionStockPartHS = new Hashtable();
		int currentPupulationStockPartSize = population.size(); 
		for(int i=0; i<mutatioGeneOnStockPart; i++){
			int moveOutGroup = (int)(population.get(""+0).groupPart.size()*Math.random());
			int moveinGroup;
			do{
				moveinGroup = (int)(population.get(""+0).groupPart.size()*Math.random());
			}while(moveOutGroup==moveinGroup);
			
			chro = copyOneChromosome(population.get(""+(int)(Math.random()*pSize)));
			
			String st = chro.groupPart.get(""+moveOutGroup).toString();
			String[] stArr=st.split(","); 
			String st1 = chro.groupPart.get(""+moveinGroup).toString();
			String[] stArr1=st1.split(",");
//				System.out.println("Before st="+ st);
//				System.out.println("Before st1="+ st1);
			if(stArr.length!=1 && stArr1.length!=1){
				if(stArr.length <= stArr1.length){
					st = st + stArr1[stArr1.length-1]+",";
//						st1 = st1.replace(stArr1[stArr1.length-1]+",", "");
					stArr1[stArr1.length-1]="";
					st1 = "";
					for(int j=0;j<stArr1.length;j++)
						if(stArr1[j]!="")  st1 += stArr1[j]+","; 
				
				}else{
					st1 = st1 + stArr[stArr.length-1]+",";
//						st = st.replace(stArr[stArr.length-1]+",", "");
					stArr[stArr.length-1]="";
					st = "";
					for(int j=0;j<stArr.length;j++)
						if(stArr[j]!="")  st += stArr[j]+","; 
				}
				chro.groupPart.put(""+moveOutGroup, st);
				chro.groupPart.put(""+moveinGroup, st1);
				
				population.put(""+currentPupulationSize, chro);
				currentPupulationSize++;
			}
		}
		return population;
	}

	static Hashtable<String, chromosome> executeInversionOperator(Hashtable<String, chromosome> population, double inverstionRate, int pSize) {
		int inversionCount = (int)(pSize*inverstionRate);
		
		int currentPupulationSize = population.size(); 
		//找出不重複的交配染色體
		int inversionNumber[]=new int[inversionCount];
		for(int i=0; i<inversionCount; i++)	{
			inversionNumber[i]=(int)(Math.random()*pSize);
			for(int j=0; j<i; j++){
				if(inversionNumber[j]==inversionNumber[i]) i--;
			}
		}
		
		for(int i=0; i<inversionCount; i++){
			chromosome chro1 = copyOneChromosome(population.get(""+inversionNumber[i]));
			int inversionGroup1 = (int)(chro1.groupPart.size()*Math.random());
			int inversionGroup2;
			do{
				inversionGroup2 = (int)(chro1.groupPart.size()*Math.random());
			}while(inversionGroup1==inversionGroup2);
			
			Object oj = chro1.groupPart.get(""+inversionGroup1);
			Object oj1 = chro1.groupPart.get(""+inversionGroup2);
			
			chro1.groupPart.put(""+inversionGroup1, oj1);
			chro1.groupPart.put(""+inversionGroup2, oj);
			population.put(""+currentPupulationSize, chro1);
			currentPupulationSize++;
		}

		return population;
	}
		
	private static double printAChromosome(Hashtable<String, chromosome> population, int i, Hashtable<String, Hashtable> input, BufferedWriter finalr, int maxCaptial,double stoppp,double stoplose) throws NumberFormatException, IOException {
		//   double avgReturn, avgTime, avgPPT, avgMDD;
		double b=0;double a=0;
		double total[]=new double[1];
		double sumtotal0=0;
		double sumROI=0;double ROI=0;
		String STOPP=stoppp+","+stoplose;

		Hashtable s2 = input.get(STOPP);
		double[][] inputData=(double[][]) s2.get("0");//training

		int stockName[]=new int[inputData.length];
		for(int hh=0;hh<inputData.length;hh++){
			stockName[hh]=(int)(inputData[hh][0]);
		}

		Hashtable htt = (Hashtable) population.get(""+i).groupPart;
		String[][] sst = new String[htt.size()][];
		for(int k=0; k<htt.size();k++){
				//	System.out.println("sssA="+population.get(""+j).groupPart.get(""+k));
			sst[k] = population.get(""+i).groupPart.get(""+k).toString().split(",");
		}
		ArrayList<String> possibleStockCombination = new ArrayList<String>();
		possibleStockCombination = getCombination(sst, htt.size());
		ArrayList<String[]> listnum = new ArrayList<String[]>();//放每個資金,ROI和哪些策略
		for(int l=0; l<possibleStockCombination.size(); l++){
			// System.out.println("=--="+possibleStockCombination.get(l));
			String[] stockCombi =  possibleStockCombination.get(l).split(",");
			ROI=0;
			double money=0;
			String TSname="";
			for(int r=0;r<stockCombi.length;r++){
				if(population.get(""+i).strategyweight.get(r+2).getClass() == Double.class){
					b = (double) population.get(""+i).strategyweight.get(r+2);
				}else{
					b = Double.parseDouble((String) population.get(""+i).strategyweight.get(r+2));
				}

				a=inputData[Integer.parseInt(stockCombi[r])][2]*b*maxCaptial;
				if(inputData[Integer.parseInt(stockCombi[r])][2]==0){
					maxCaptial=0;
				}
				money=money+(b*maxCaptial);
				ROI=ROI+a;
				TSname =TSname+(stockName[Integer.parseInt(stockCombi[r])]+",");
			}
			String nuum[]=new String[3];
			nuum[0]=String.valueOf(ROI);
			nuum[1]=String.valueOf(money);
			nuum[2]=TSname;
			sumROI=sumROI+ROI;
		//	 System.out.println("sumROI "+sumROI);
		// sumROI=0;
			listnum.add(nuum);
		}
		double min=999999999;
		double max=-999999999;
		String witchname="";
		String witchname1="";
		String mon="";
		String mon1="";

		for(int w=0;w<listnum.size();w++){
			String[] a1 =listnum.get(w);
			if(Double.valueOf(a1[0])<min){
				min=Double.valueOf(a1[0]);
				witchname=a1[2];
				mon=a1[1];
			}
			if(Double.valueOf(a1[0])>max){
				max=Double.valueOf(a1[0]);
				witchname1=a1[2];
				mon1=a1[1];
			}
			System.out.println("ai "+a1 [0]+"///"+a1[1]+"///"+a1[2]);
			 
		}
		System.out.println(min+" MAX="+max+" "+ witchname+"11"+ witchname1+" "+ mon+" "+mon1);
		 
		finalr.write(" MAX="+max+ " TS="+witchname1+" Cap="+ mon1);
		finalr.newLine();
		finalr.write(" Min="+min+ " TS="+witchname+" Cap="+ mon);
	//	System.out.println("ROI "+ROI);
	//	System.out.println("測試"+possibleStockCombination.size()); 
		System.out.println("++,"+sumROI/possibleStockCombination.size());
//						double variance=va(listnum,(sumROI/possibleStockCombination.size()));
		finalr.newLine();
//						 finalr.write(" VAR="+variance);
		int countsum=1;	 
		for(int j=0; j<population.get(""+i).groupPart.size(); j++){
/*			 avgTime =0;
			 avgReturn =0;
			 avgPPT =0;
			 avgMDD =0;*/
			 //System.out.print(population.get(""+i).groupPart.get(""+j)+" ");
			 Hashtable ht = (Hashtable) population.get(""+i).groupPart;
			System.out.print("G"+(j+1)+": ");
			String[] st = ht.get(""+j).toString().split(",");
			for(int k=0; k<st.length;k++){
				 System.out.print("strategyName"+stockName[Integer.parseInt(st[k])]+" ");
				 finalr.write("strategyName"+stockName[Integer.parseInt(st[k])]+" ");
			
			}
			System.out.println();
			finalr.newLine();
		}
		for(int j=0; j<population.get(""+i).strategyweight.size(); j++){
			 System.out.printf(" "+(population.get(""+i).strategyweight.get(j).toString()));
			 finalr.write(" "+(population.get(""+i).strategyweight.get(j).toString()));
		}
		finalr.newLine();
		System.out.println();

		System.out.printf("Fitness Value=%.2f ", population.get(""+i).fitness[0]);
		finalr.write(" Fitness Value= "+ population.get(""+i).fitness[0]);
		System.out.printf(" ROI=%.2f ", population.get(""+i).fitness[1]);
		finalr.write(" ROI= "+ population.get(""+i).fitness[1]);
		System.out.printf(" Group Balance=%.2f ", population.get(""+i).fitness[2]);
		finalr.write(" Group Balance= "+ population.get(""+i).fitness[2]);
		System.out.printf(" Risk=%.2f", population.get(""+i).fitness[3]);
		finalr.write(" Risk="+ population.get(""+i).fitness[3]);
		System.out.println(" Weight Balance="+ population.get(""+i).fitness[4]);
		finalr.write(" Weight Balance="+ population.get(""+i).fitness[4]);
		finalr.newLine();
		System.out.printf("平均一組策略報酬1: "+ population.get(""+i).fitness[1]);
		finalr.write("平均一組策略報酬1: "+ population.get(""+i).fitness[1]);
		return population.get(""+i).fitness[1];
	}
	private static boolean C(Hashtable<String, chromosome> population, int i) {//如果group有一個一組的話回傳FALSE
		// TODO Auto-generated method stub
		int a=0;
		Hashtable htt = (Hashtable) population.get(""+i).groupPart;
		
		String[][] sst = new String[htt.size()][];
		for(int k=0; k<htt.size();k++){
			sst[k] = population.get(""+i).groupPart.get(""+k).toString().split(",");
		}
		 
		for(int k=0; k<htt.size();k++){
			if(sst[k].length==1){
				a++;
			}
		}
		if(a>=1)
			return false;
		else
			return true;
	}
		
		
	private static double[] printAChromosome1(Hashtable<String, chromosome> population, int i, Hashtable<String, Hashtable> input, BufferedWriter finalr, int maxCaptial,double stoppp,double stoplose) throws NumberFormatException, IOException  {
		// TODO Auto-generated method stub
		double aa[]=new double[7];
		double a=0;
		double b=0;
		double c=0;
		double ROI=0;
		double sumROI=0;
		double sumcap=0;

		String STOPP=stoppp+","+stoplose;
		Hashtable s2 = input.get(STOPP);
		double[][] inputData=(double[][]) s2.get("1");//testing
	  
		int stockName[]=new int[inputData.length];
		for(int hh=0;hh<inputData.length;hh++){
			stockName[hh]=(int)(inputData[hh][0]);
		}

		Hashtable htt = (Hashtable) population.get(""+i).groupPart;
		String[][] sst = new String[htt.size()][];
		for(int k=0; k<htt.size();k++){
			//System.out.println("sssA="+population.get(""+j).groupPart.get(""+k));
			sst[k] = population.get(""+i).groupPart.get(""+k).toString().split(",");
		}

		ArrayList<String> possibleStockCombination = new ArrayList<String>();
		possibleStockCombination = getCombination(sst, htt.size());
		ArrayList<String[]> listnum = new ArrayList<String[]>();//放每個資金,ROI和哪些策略
				
		for(int l=0; l<possibleStockCombination.size(); l++){
			String TSname="" ;
			ROI=0; double cap=0;double Ccap=0;
			String[] stockCombi =  possibleStockCombination.get(l).split(",");
			for(int r=0;r<stockCombi.length;r++){
				if(population.get(""+i).strategyweight.get(r+2).getClass() == Double.class){
					b = (double) population.get(""+i).strategyweight.get(r+2);
				}else{
					b = Double.parseDouble((String) population.get(""+i).strategyweight.get(r+2));
				}
				a=inputData[Integer.parseInt(stockCombi[r])][2]*b;
				ROI=ROI+(a*maxCaptial);
				if(inputData[Integer.parseInt(stockCombi[r])][2]==0){
					b=0;
				}
				cap=cap+(b*maxCaptial);
				
				TSname =TSname+(stockName[Integer.parseInt(stockCombi[r])]+",");
			}
			String nuum[]=new String[4];
			nuum[0]=String.valueOf(ROI);
			nuum[1]=String.valueOf(cap);
			nuum[2]=TSname;
			if(cap==0){
				nuum[3]="0.00";	
			}
			if(cap!=0){
				nuum[3]=String.valueOf(ROI/cap);
			}
			listnum.add(nuum);
			sumROI=sumROI+ROI;
			sumcap=sumcap+cap;
			System.out.print("dd"+ROI+",");
			System.out.println("dd"+cap);
	//	System.out.println("d "+nuum[3]);
		}

		double min=999999999;
		double max=-999999999;
		String witchname="";
		String ro="";
		String ro1="";
		String witchname1="";
		String mon="";
		String mon1="";
		double ss=0;
//算最大最小值
		for(int w=0;w<listnum.size();w++){
			String[] a1 =listnum.get(w);
			ss+=Double.valueOf(a1[3]);
			if(Double.valueOf(a1[3])<min){
				min=Double.valueOf(a1[3]);
				ro=a1[0];
				witchname=a1[2];
				mon=a1[1];
			}
			if(Double.valueOf(a1[3])>max){
				max=Double.valueOf(a1[3]);
				witchname1=a1[2];
				mon1=a1[1];
				ro1=a1[0];
			}
			System.out.println("ai "+a1 [0]+"///"+a1[1]+"///"+a1[2]);
			System.out.println("ss "+ss);
				
		}
		System.out.println(min+" MAX"+max+" "+ witchname+"11"+" "+ro+"  "+ro1+ witchname1+" "+ mon+" "+mon1);
		finalr.newLine();
		finalr.write(" MAX="+max+" MAXROI="+ro1+"  MAXTS="+witchname1+" MAXCap="+ mon1);
		finalr.newLine();
		finalr.write(" Min="+min+" MinROI="+ro+ "  MinTS="+witchname+" MinCap="+ mon);
		finalr.newLine();
//					System.out.println("測試"+possibleStockCombination.size()+"  "+ss/listnum.size()+"R"+sumROI/possibleStockCombination.size()+" C  "+sumcap/possibleStockCombination.size());
		 
//					c=Double.parseDouble((population.get(""+i).strategyweight.get(1).toString()))*maxCaptial;
		System.out.println("平均:"+ss/listnum.size()); 
		finalr.write("平均:"+ss/listnum.size()); 
		double variance=va(listnum,ss/listnum.size());
		finalr.newLine();
		 finalr.write(" VAR="+variance);
		finalr.newLine();
		finalr.newLine();
		finalr.newLine();

		aa[0]=ss/listnum.size();//平均
		
		if(Double.valueOf(mon1)==0){
			aa[1]=0.00;
		}
		if(Double.valueOf(mon1)!=0){
			aa[1]=Double.valueOf(ro1)/Double.valueOf(mon1);//最大
		}
		if(Double.valueOf(mon)==0){
			aa[2]=0.00;
		}
		if(Double.valueOf(mon)!=0){
			aa[2]=Double.valueOf(ro)/Double.valueOf(mon);
		}
		return aa;
	}
		
	private static double va(ArrayList<String[]> listnum, double s) {
		// TODO Auto-generated method stub
		double var=0;
		for(int w=0;w<listnum.size();w++){
			String[] a1 =listnum.get(w);
			var+=Math.pow((Double.valueOf(a1[3])-s),2);
		}
		System.out.println("VAR"+var); 
		System.out.println(var/(listnum.size()-1));
		return var/(listnum.size()-1);
	}

	private static double va(double[] avgnum, double d) {
		// TODO Auto-generated method stub
		double var=0;
		for(int i=0;i<avgnum.length;i++){
			var+=Math.pow(((avgnum[i]*100)-d),2);
		}
		System.out.println(var/(avgnum.length-1));
		return var/(avgnum.length-1);
	}

	private static Hashtable<String, Hashtable> pop1( double stopPP, double stoplose, String[][] inputDataTEC, String[][] inputTestfileTEC, int num, int chooseReturnRate, int chooseMDD, int choosecount,int num1, Hashtable<String, Hashtable> input1) {
		// TODO Auto-generated method stub
		double RankReturnRate[]=new double[100];
		double Rank1ReturnRate[]=new double[100];
		double Rank1[][]=new double[100][6];
		double RankMDD[]=new double[100];
		double Rank1MDD[]=new double[100];
		double Rankcount[]=new double[100];
		double Rank1count[]=new double[100];
		int co=7;

		String stopp=stopPP+","+stoplose;
		System.out.println( "*&**"+stopPP+","+stoplose);
		ArrayList<Integer> alre=new ArrayList<>();
		
		while(co!=107){
			//System.out.println(co+","+"co");
			ArrayList<String[]>str= STR11(inputDataTEC, num,co,stopPP,stoplose);
			if(stopPP==0.0 && stoplose==-0.0){
				str= STR(inputDataTEC, num,co);
			}
			for(int i=0;i<str.size();i++){
				String aaa[]=str.get(i);
			//System.out.println(aaa[1]+" "+aaa[2]+" "+aaa[3]);
			}
			if(str.size()==0){
				//System.out.println("NULL");
				RankReturnRate[co-7]=-999999;
				RankMDD[co-7]=-999999;
				Rankcount[co-7]=999999;
				Rank1ReturnRate[co-7]=co-6;
				Rank1MDD[co-7]=co-6;
				Rank1count[co-7]=co-6;
				Rank1[co-7][0]=co-6;
				Rank1[co-7][1]=-999999;
				Rank1[co-7][2]=-999999;
				Rank1[co-7][3]=999999;
				Rank1[co-7][4]=-999999;
				Rank1[co-7][5]=-999999;
			}
			else{
				int Count =count(str);
				double ReturnRate=mareturnrate(str);
				double ReturnRate1=mareturnrate1(str);
				double MDD=MDD(str,Count);//價差取最大客略虧損
				double MDD1=MDD1(str,Count);//以前的
			//System.out.println(num+","+Count+","+Return+","+Return1+","+ReturnRate+","+ReturnRate1+","+PPT+","+PPT1+","+count1+","+count2+","+WinRate+","+WinRate1+","+WinAve+","+WinAve1+","+LosAve+","+LosAve1+","+MDD+","+tax+","+onceReturnRate);
			//System.out.println("OOO"+PF);
				RankReturnRate[co-7]=ReturnRate1;
				RankMDD[co-7]=MDD1;
				Rankcount[co-7]=Count;
				Rank1ReturnRate[co-7]=co-6;
				Rank1MDD[co-7]=co-6;
				Rank1count[co-7]=co-6;
				//Rank1[co-46][1]=ReturnRate;
				Rank1[co-7][0]=co-6;//第幾個策略
				Rank1[co-7][1]=ReturnRate;
				Rank1[co-7][2]=MDD;
				Rank1[co-7][3]=Count;
				Rank1[co-7][4]=ReturnRate1;
				Rank1[co-7][5]=MDD1;
				System.gc();
			}
			co++;
		}
		for (int i =  RankReturnRate.length - 1; i > 0; --i)
			for (int j = 0; j < i; ++j)
				if (RankReturnRate[j] < RankReturnRate[j + 1]){
					Swap(RankReturnRate, j, j + 1);
					Swap(Rank1ReturnRate, j, j + 1);
				}
		alre=RReturnRate(RankReturnRate,Rank1ReturnRate,chooseReturnRate,alre);
		System.gc();

		double Rank1bMDD[] = new double[RankMDD.length-alre.size()];
		double RankbMDD[] = new double[RankMDD.length-alre.size()];

		int c=0;
		for(int i=0;i<Rank1MDD.length;i++){
			if(alre.contains((int)(Rank1MDD[i])))
				continue;
			else{
				Rank1bMDD[c]=Rank1MDD[i];
				RankbMDD[c]=RankMDD[i];
				c++;
			}
		}

		for (int i =  RankbMDD.length - 1; i > 0; --i)
			for (int j = 0; j < i; ++j)
				if ( RankbMDD[j] < RankbMDD[j + 1]){
					Swap(RankbMDD, j, j + 1);
					Swap(Rank1bMDD, j, j + 1);
				}
		alre=RReturnRate(RankbMDD,Rank1bMDD,chooseMDD,alre);
		double Rank1bcount[]=new double[Rankcount.length-alre.size()];
		double Rankbcount[]=new double[Rankcount.length-alre.size()];
		int d=0;
		for(int i=0;i<Rank1count.length;i++){
			if(alre.contains((int)(Rank1count[i])))
				continue;
			else{
				Rank1bcount[d]=Rank1count[i];
				Rankbcount[d]=Rankcount[i];
				d++;
			}
		}
		for (int i =  Rankbcount.length - 1; i > 0; --i)
			for (int j = 0; j < i; ++j)
				if ( Rankbcount[j] > Rankbcount[j + 1]){
					Swap(Rankbcount, j, j + 1);
					Swap(Rank1bcount, j, j + 1);
				}
		//for(int i=0;i<Rank1bcount.length;i++){
		//	System.out.println("i"+i+","+"R"+Rank1bcount[i]+","+Rankbcount[i]);
		//}
		alre=RReturnRate1(Rankbcount,Rank1bcount,choosecount,alre);
		System.out.println(alre);
		double storea[][]=new double[alre.size()][4];
		double storeb[][]=new double[alre.size()][4];
			
		 Hashtable<String,double[][]> store = new Hashtable<String,double[][]>();
		for(int i=0;i<alre.size();i++){
			co=alre.get(i);//第幾個策略(從15個策略選出)
			storea[i][0]=co;//第幾個策略
			storea[i][1]=Rank1[co-1][3];
			storea[i][2]=Rank1[co-1][4];
			storea[i][3]=Rank1[co-1][5];
			if(storea[i][1]==999999||storea[i][2]==-999999||storea[i][3]==-999999){
				storea[i][0]=co;//第幾個策略
				storea[i][1]=0;
				storea[i][2]=0;
				storea[i][3]=0;
			}
			co=co+6;
			// System.out.println(co+","+"co11");
			ArrayList<String[]>str1= STR11(inputTestfileTEC, num1,co,stopPP,stoplose);
			if(Double.valueOf(stopPP)==0.00 && Double.valueOf(stoplose)==-0.00){
				str1= STR(inputTestfileTEC, num1,co);
			}
			if(str1.size()==0){
				storeb[i][0]=co-6;//第幾個策略(1-15)
				storeb[i][1]=0;
				storeb[i][2]=0;
				storeb[i][3]=0;
			}
			else{
				int Count =count(str1);
				double ReturnRate=mareturnrate(str1);
				double ReturnRate1=mareturnrate1(str1);
				double MDD=MDD(str1,Count);//價差取最大策略虧損
				double MDD1=MDD1(str1,Count);//價差取最大策略虧損-tax
				storeb[i][0]=co-6;
				storeb[i][1]=Count;
				storeb[i][2]=ReturnRate1;
				storeb[i][3]=MDD1;
			}
		}
//	 	String Point=population.get(""+p).point.get(1)+","+stoplose;
		store.put(""+0,storea);
		store.put(""+1,storeb);
		input1.put(""+stopp,store);
		Enumeration<String> e = input1.keys();
		while(e. hasMoreElements()){
			String s= e.nextElement().toString();
			Hashtable s2 = input1.get(s);
			System.out.println(s);
		}
		return input1;
	}
}