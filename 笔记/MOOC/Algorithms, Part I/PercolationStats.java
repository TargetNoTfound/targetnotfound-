import edu.princeton.cs.algs4.StdRandom;
import edu.princeton.cs.algs4.StdStats;
import java.lang.Math.*;

public class PercolationStats {
  private int n;
  private int trials;
  private double[] experiments;
  private double meanOfExper;
  private double stddevOfExper;
  
  public PercolationStats(int n, int trials) {
    // perform trials independent experiments on an n-by-n grid
	if (n <= 0 || trials <= 0) {
	  throw new java.lang.IllegalArgumentException("n ≤ 0 or trials ≤ 0");
	}  
    this.n = n;
    this.trials = trials;
    experiments = new double[trials];
    Percolation percSample ;
    for (int i = 0; i < trials; i++) {
      percSample = new Percolation(n);
      while (!percSample.percolates()) {
    	int row = StdRandom.uniform(1, n + 1) ,col = StdRandom.uniform(1, n + 1);
        percSample.open(row ,col );
      }
      experiments[i] = percSample.numberOfOpenSites() * 1.0 / n / n;
    }
    meanOfExper = StdStats.mean(experiments);
    stddevOfExper = StdStats.stddev(experiments);
  }
   
  public double mean() {
    // sample mean of percolation threshold
    return meanOfExper;
  }
   
  public double stddev() {
    // sample standard deviation of percolation threshold
    return stddevOfExper;
  }
  
  public double confidenceLo() {
    // low  endpoint of 95% confidence interval
    return (meanOfExper - (1.96 * stddevOfExper / Math.sqrt(trials)));
  }
  
  public double confidenceHi() {
    // high endpoint of 95% confidence interval
    return (meanOfExper + (1.96 * stddevOfExper / Math.sqrt(trials)));
  }

  public static void main(String[] args) {
    // test client (described below)
    int n = Integer.parseInt(args[0]);
    int trials = Integer.parseInt(args[1]);
    PercolationStats perc = new PercolationStats(n, trials);
    System.out.printf("mean                    = %f\n" , perc.meanOfExper);
    System.out.printf("stddev                  = %.17f\n" , perc.stddevOfExper);
    System.out.print("95% ");
    System.out.printf("confidence interval = [%.16f, %.16f]\n", perc.confidenceLo(),  
                                                                   perc.confidenceHi());
  }
}