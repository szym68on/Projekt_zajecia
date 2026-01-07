import org.graphstream.graph.*;
import org.graphstream.graph.implementations.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Basic Graph Viewer for Football Team Evolution
 * Visualizes player co-occurrence graphs using GraphStream
 */
public class GraphViewer {
    
    private Graph graph;
    
    // CSS styling for the graph
    private static final String GRAPH_STYLE = 
        "node {" +
        "   fill-color: #4A90E2;" +
        "   size: 20px;" +
        "   text-size: 14;" +
        "   text-alignment: above;" +
        "   text-background-mode: rounded-box;" +
        "   text-background-color: white;" +
        "   text-padding: 3px;" +
        "}" +
        "edge {" +
        "   fill-color: #CCCCCC;" +
        "   size: 2px;" +
        "}";
    
    public GraphViewer() {
        // Use Swing viewer
        System.setProperty("org.graphstream.ui", "swing");
        
        graph = new SingleGraph("Football Team Evolution");
        graph.setAttribute("ui.stylesheet", GRAPH_STYLE);
        graph.setAttribute("ui.quality");
        graph.setAttribute("ui.antialias");
    }
    
    /**
     * Load graph from text file
     * Format: EDGE player1 | player2 | weight | matches1 | matches2
     */
    public void loadGraph(String filePath) throws IOException {
        System.out.println("📂 Loading graph from: " + filePath);
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                
                // Skip comments and empty lines
                if (line.startsWith("#") || line.isEmpty()) {
                    continue;
                }
                
                // Parse edge line
                if (line.startsWith("EDGE")) {
                    parseEdge(line);
                }
            }
            
            System.out.println("✅ Graph loaded!");
            System.out.println("   Players: " + graph.getNodeCount());
            System.out.println("   Connections: " + graph.getEdgeCount());
        }
    }
    
    /**
     * Parse edge: EDGE player1 | player2 | weight | matches1 | matches2
     */
    private void parseEdge(String line) {
        // Remove "EDGE " prefix
        line = line.substring(5);
        
        // Split by |
        String[] parts = line.split("\\|");
        if (parts.length < 5) {
            return;
        }
        
        String player1 = parts[0].trim();
        String player2 = parts[1].trim();
        int weight = Integer.parseInt(parts[2].trim());
        int matches1 = Integer.parseInt(parts[3].trim());
        int matches2 = Integer.parseInt(parts[4].trim());
        
        // Add nodes if they don't exist
        if (graph.getNode(player1) == null) {
            Node node = graph.addNode(player1);
            node.setAttribute("ui.label", player1);
            node.setAttribute("matches", matches1);
            // Node size based on matches
            int nodeSize = Math.max(15, matches1 / 2);
            node.setAttribute("ui.style", "size: " + nodeSize + "px;");
        }
        
        if (graph.getNode(player2) == null) {
            Node node = graph.addNode(player2);
            node.setAttribute("ui.label", player2);
            node.setAttribute("matches", matches2);
            int nodeSize = Math.max(15, matches2 / 2);
            node.setAttribute("ui.style", "size: " + nodeSize + "px;");
        }
        
        // Add edge
        String edgeId = player1 + "-" + player2;
        Edge edge = graph.addEdge(edgeId, player1, player2);
        edge.setAttribute("weight", weight);
        // Edge thickness based on weight
        int edgeSize = Math.max(1, weight / 10);
        edge.setAttribute("ui.style", "size: " + edgeSize + "px;");
    }
    
    /**
     * Display the graph
     */
    public void display() {
        graph.display();
    }
    
    /**
     * Main method
     */
    public static void main(String[] args) {
        // Default: Barcelona 2015/2016
        String defaultPath = "../graphs/fc_barcelona_2015_2016_graph.txt";
        String graphFile = args.length > 0 ? args[0] : defaultPath;
        
        try {
            GraphViewer viewer = new GraphViewer();
            viewer.loadGraph(graphFile);
            viewer.display();
            
            System.out.println("\n📊 Graph displayed!");
            System.out.println("💡 Use mouse to zoom and drag nodes");
            
        } catch (IOException e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}