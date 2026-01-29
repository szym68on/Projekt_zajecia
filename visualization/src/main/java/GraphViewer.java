import org.graphstream.graph.*;
import org.graphstream.graph.implementations.*;
import org.graphstream.ui.swing_viewer.SwingViewer;
import org.graphstream.ui.view.Viewer;
import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.List;

/**
 * Main application window for Football Team Evolution visualization
 */
public class GraphViewer extends JFrame {
    private static final String GRAPHS_DIR = "../graphs";
    
    private Graph graph;
    private Viewer viewer;
    private JComboBox<String> clubComboBox;
    private JComboBox<String> seasonComboBox;
    private StatsPanel statsPanel;
    private DynamicScoreLoader scoreLoader;
    
    private String[] clubs = {
        "athletic_bilbao",
        "atletico_madryt",
        "fc_barcelona",
        "real_madryt",
        "villarreal_cf"
    };
    
    private String[] seasons;

    public GraphViewer() {
        super("Football Team Evolution - Graph Viewer");
        
        // Initialize seasons (2005-2024)
        List<String> seasonList = new ArrayList<>();
        for (int year = 2005; year < 2025; year++) {
            seasonList.add(year + "_" + (year + 1));
        }
        seasons = seasonList.toArray(new String[0]);
        
        // Load DynamicScore data
        scoreLoader = new DynamicScoreLoader();
        
        // Initialize graph
        System.setProperty("org.graphstream.ui", "swing");
        graph = new SingleGraph("FootballTeam");
        graph.setAttribute("ui.stylesheet", getStyleSheet());
        graph.setAttribute("ui.quality");
        graph.setAttribute("ui.antialias");
        
        // Setup UI
        setupUI();
        
        // Load default graph
        loadGraph("fc_barcelona", "2015_2016");
        
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1400, 800);
        setLocationRelativeTo(null);
    }

    private void setupUI() {
        setLayout(new BorderLayout(10, 10));
        
        // Top control panel
        JPanel controlPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 10));
        controlPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
        
        // Club selector
        controlPanel.add(new JLabel("Club:"));
        clubComboBox = new JComboBox<>(clubs);
        clubComboBox.setSelectedItem("fc_barcelona");
        clubComboBox.addActionListener(e -> onClubOrSeasonChanged());
        controlPanel.add(clubComboBox);
        
        // Season selector
        controlPanel.add(new JLabel("Season:"));
        seasonComboBox = new JComboBox<>(seasons);
        seasonComboBox.setSelectedItem("2015_2016");
        seasonComboBox.addActionListener(e -> onClubOrSeasonChanged());
        controlPanel.add(seasonComboBox);
        
        // Load button
        JButton loadButton = new JButton("Load");
        loadButton.addActionListener(e -> {
            String club = (String) clubComboBox.getSelectedItem();
            String season = (String) seasonComboBox.getSelectedItem();
            loadGraph(club, season);
        });
        controlPanel.add(loadButton);

        // Timeline button
        JButton timelineButton = new JButton("Timeline");
        timelineButton.addActionListener(e -> {
            String club = (String) clubComboBox.getSelectedItem();
            openTimelineWindow(club);
        });
        controlPanel.add(timelineButton);
        
        add(controlPanel, BorderLayout.NORTH);
        
        // Center: Graph viewer
        viewer = new SwingViewer(graph, Viewer.ThreadingModel.GRAPH_IN_ANOTHER_THREAD);
        viewer.enableAutoLayout();
        Component viewPanel = (Component) viewer.addDefaultView(false);
        add(viewPanel, BorderLayout.CENTER);
        
        // Right: Stats panel
        statsPanel = new StatsPanel();
        add(statsPanel, BorderLayout.EAST);
    }

    private void onClubOrSeasonChanged() {
        // Update season dropdown based on club
        // (all clubs have same seasons, but could filter if needed)
    }

    private void loadGraph(String club, String season) {
        String filename = String.format("%s/%s_%s_graph.txt", GRAPHS_DIR, club, season);
        
        File file = new File(filename);
        if (!file.exists()) {
            JOptionPane.showMessageDialog(this,
                "File not found: " + filename,
                "Error",
                JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        graph.clear();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                
                // Skip comments and empty lines
                if (line.isEmpty() || line.startsWith("#")) {
                    continue;
                }
                
                // Parse EDGE lines
                if (line.startsWith("EDGE")) {
                    parseEdge(line.substring(5).trim());
                }
            }
            
            // Update stats panel with DynamicScore data
            DynamicScoreData prevTransition = scoreLoader.getTransitionTo(club, season);
            DynamicScoreData nextTransition = scoreLoader.getTransition(club, season);
            statsPanel.updateStats(graph, club, season, prevTransition, nextTransition);
            
            setTitle("Football Team Evolution - " + formatClubName(club) + " " + formatSeason(season));
            
            System.out.println("Loaded graph: " + club + " " + season);
            System.out.println("Nodes: " + graph.getNodeCount() + ", Edges: " + graph.getEdgeCount());
            
        } catch (IOException e) {
            JOptionPane.showMessageDialog(this,
                "Error loading file: " + e.getMessage(),
                "Error",
                JOptionPane.ERROR_MESSAGE);
            e.printStackTrace();
        }
    }

    private void parseEdge(String line) {
        String[] parts = line.split("\\|");
        if (parts.length < 5) {
            return;
        }
        
        String player1 = parts[0].trim();
        String player2 = parts[1].trim();
        int weight = Integer.parseInt(parts[2].trim());
        int matches1 = Integer.parseInt(parts[3].trim());
        int matches2 = Integer.parseInt(parts[4].trim());
        
        // Add or get nodes
        Node node1 = graph.getNode(player1);
        if (node1 == null) {
            node1 = graph.addNode(player1);
            node1.setAttribute("ui.label", player1);
            node1.setAttribute("matches", matches1);
            
            // Medium node size - balanced
            int nodeSize = Math.min(40, Math.max(18, matches1 / 2));
            
            // Color based on matches (more matches = darker blue)
            String color = getNodeColor(matches1);
            node1.setAttribute("ui.style", String.format(
                "size: %dpx; fill-color: %s; stroke-color: #1a3a6e;", 
                nodeSize, color));
        }
        
        Node node2 = graph.getNode(player2);
        if (node2 == null) {
            node2 = graph.addNode(player2);
            node2.setAttribute("ui.label", player2);
            node2.setAttribute("matches", matches2);
            
            // Medium node size - balanced
            int nodeSize = Math.min(40, Math.max(18, matches2 / 2));
            
            // Color based on matches
            String color = getNodeColor(matches2);
            node2.setAttribute("ui.style", String.format(
                "size: %dpx; fill-color: %s; stroke-color: #1a3a6e;", 
                nodeSize, color));
        }
        
        // Add edge
        String edgeId = player1 + "-" + player2;
        if (graph.getEdge(edgeId) == null) {
            Edge edge = graph.addEdge(edgeId, player1, player2);
            edge.setAttribute("weight", weight);
            
            // Thinner edges for cleaner look
            int edgeSize = Math.min(5, Math.max(1, weight / 12));
            String edgeColor = getEdgeColor(weight);
            edge.setAttribute("ui.style", String.format(
                "size: %dpx; fill-color: %s;", 
                edgeSize, edgeColor));
        }
    }

    private String getEdgeColor(int weight) {
        // Color gradient from light gray (weak connection) to dark gray (strong connection)
        if (weight >= 35) return "#333333";       // Very strong partnership
        if (weight >= 25) return "#555555";       // Strong partnership
        if (weight >= 15) return "#777777";       // Medium partnership
        if (weight >= 5) return "#999999";        // Weak partnership
        return "#bbbbbb";                         // Very weak partnership
    }

    private String getStyleSheet() {
        return 
            "graph {" +
            "   fill-color: #ffffff;" +
            "   padding: 70px;" +
            "}" +
            "node {" +
            "   fill-mode: gradient-radial;" +
            "   fill-color: #4a90e2, #2c5aa0;" +
            "   stroke-mode: plain;" +
            "   stroke-color: #1a3a6e;" +
            "   stroke-width: 2px;" +
            "   shadow-mode: plain;" +
            "   shadow-color: #00000030;" +
            "   shadow-width: 3px;" +
            "   shadow-offset: 2px;" +
            "   text-size: 17px;" +                            // Larger text
            "   text-style: bold;" +
            "   text-color: #000000;" +                        // Black for contrast
            "   text-alignment: under;" +
            "   text-background-mode: rounded-box;" +
            "   text-background-color: #fffffff0;" +           // Almost opaque white
            "   text-padding: 7px, 4px;" +                     // More padding
            "   text-offset: 0px, 7px;" +
            "   text-border-mode: plain;" +
            "   text-border-width: 2px;" +                     // Thicker border
            "   text-border-color: #888888;" +                 // Darker gray border
            "}" +
            "edge {" +
            "   fill-color: #888888;" +
            "   arrow-shape: none;" +
            "   shadow-mode: plain;" +
            "   shadow-color: #00000020;" +
            "   shadow-width: 1px;" +
            "   shadow-offset: 1px;" +
            "}";
    }

    private String getNodeColor(int matches) {
        // Color gradient from light blue (few matches) to dark blue (many matches)
        if (matches >= 40) return "#1a4d99";      // Dark blue - key players
        if (matches >= 30) return "#2c5aa0";      // Medium-dark blue
        if (matches >= 20) return "#4a90e2";      // Medium blue
        if (matches >= 10) return "#6ba3e8";      // Light-medium blue
        return "#8bbff0";                         // Light blue - substitute players
    }

    private String formatClubName(String club) {
        return club.replace("_", " ").toUpperCase();
    }

    private String formatSeason(String season) {
        return season.replace("_", "/");
    }

    private void openTimelineWindow(String club) {
        TimelineWindow timelineWindow = new TimelineWindow(club, scoreLoader);
        timelineWindow.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            GraphViewer viewer = new GraphViewer();
            viewer.setVisible(true);
        });
    }
}
