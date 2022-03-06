
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;


public class chromosome
{
		Hashtable groupPart = new Hashtable(); //key: group name, value: elements(stocks)
		ArrayList strategyweight = new ArrayList();
		double[] fitness = new double[6];//fitness[3]:unitBalance, fitness[4]=priceBalance, fitness[5]=diversity
}