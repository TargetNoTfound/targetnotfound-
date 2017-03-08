import edu.princeton.cs.algs4.WeightedQuickUnionUF;

public class Percolation {
  private int n;
  private boolean[][] Sites;
  private WeightedQuickUnionUF OpenSites;
  private WeightedQuickUnionUF FullOpenSites;
  private int openCount = 0;
  
  public Percolation(int n) {
    // create n-by-n grid, with all sites blocked
    if (n <= 0) {
      throw new java.lang.IllegalArgumentException("n<=0");
	}
	this.n = n;
    Sites = new boolean[n][n] ;
    OpenSites = new WeightedQuickUnionUF(n * n + 2) ;
    //所使用的数组由于在sites顶和底另外设置了一个联通分量 所以数组大小为n*n+2, [0]为顶部 [n*n+1]为底部
    FullOpenSites = new WeightedQuickUnionUF(n * n + 1);
    //为了正确得出full open site 建立另一个并查集 并且删去底节点
    
    //initialization of Sites

    for (int i = 0; i < Sites.length; i++) {
      for (int j = 0; j < Sites[i].length; j++) {
        Sites[i][j] = false;
      }
    }
  }
  
  public    void open(int row, int col) {
    // open site (row, col) if it is not open already
    if (row <= 0 || row > n || col <= 0 || col > n) {
      throw new java.lang.IndexOutOfBoundsException("out of range");
    }
    if (!Sites[row - 1][col - 1]) {
      Sites[row - 1][col - 1] = true;
      openCount++;
      //当行数等于1时 与顶节点连接
      int site = (row - 1) * n + col ;
      if (row == 1) {
        OpenSites.union(0, site ); 
        FullOpenSites.union(0, site );
      }
      if (row == n ) {
        OpenSites.union(n * n + 1, site);
      }
      if (row - 1 != 0 ) {
        if (isOpen(row - 1, col)) {
          OpenSites.union(site, (row - 2) * n + col);
          FullOpenSites.union(site, (row - 2) * n + col);
        }
      }
      if (row + 1 != n + 1 ) {
        if (isOpen(row + 1, col)) {
          OpenSites.union(site, row * n + col);
          FullOpenSites.union(site, row * n + col);
    	}
      }
      if (col - 1 != 0 ) {
    	if (isOpen(row, col - 1)) {
          OpenSites.union(site, (row - 1) * n + (col - 1));
          FullOpenSites.union(site, (row - 1) * n + (col - 1));
    	}
      }
      if (col + 1 != n + 1) {
    	if(isOpen(row, col + 1)) {
          OpenSites.union(site, (row - 1) * n + (col + 1));
          FullOpenSites.union(site, (row - 1) * n + (col + 1));
    	}
      }
    }
  }
  
  public boolean isOpen(int row, int col) {
    // is site (row, col) open?
    if (row <= 0 || row > n || col <= 0 || col > n) {
      throw new java.lang.IndexOutOfBoundsException("out of range");
    }
    return Sites[row - 1][col - 1];
  }
  
  public boolean isFull(int row, int col) {
    // is site (row, col) full?
    if (row <= 0 || row > n || col <= 0 || col > n) {
      throw new java.lang.IndexOutOfBoundsException("out of range");
    }
    return (FullOpenSites.connected(0, (row - 1) * n + col));
  }
  
  public     int numberOfOpenSites() {
    // number of open sites
    return openCount;
  }
  
  public boolean percolates() {
    // does the system percolate?
    return OpenSites.connected(0 , n * n + 1);
  }

  public static void main(String[] args) {
    // test client (optional)
  }
}