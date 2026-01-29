import javax.swing.*;
import java.awt.*;
import java.util.List;
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.Edge;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Statistics panel showing current season info and DynamicScore
 */
public class StatsPanel extends JPanel {
    private JLabel clubLabel;
    private JLabel seasonLabel;
    private JLabel playersLabel;
    private JLabel edgesLabel;
    private JLabel densityLabel;
    
    private JPanel prevScorePanel;
    private JPanel nextScorePanel;
    private JTextArea topPairsArea;
    private JTextArea topPlayersArea;

    public StatsPanel() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        setPreferredSize(new Dimension(450, 600));  // Much wider (was 350)
        setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Current season section
        add(createSectionLabel("CURRENT SEASON"));
        clubLabel = createDataLabel("");
        seasonLabel = createDataLabel("");
        add(clubLabel);
        add(seasonLabel);
        add(Box.createVerticalStrut(5));
        
        playersLabel = createDataLabel("");
        edgesLabel = createDataLabel("");
        densityLabel = createDataLabel("");
        add(playersLabel);
        add(edgesLabel);
        add(densityLabel);

        add(Box.createVerticalStrut(15));
        add(createSeparator());
        add(Box.createVerticalStrut(15));

        // DynamicScore section
        add(createSectionLabel("DYNAMIC SCORE"));
        add(Box.createVerticalStrut(10));
        
        prevScorePanel = createScorePanel();
        nextScorePanel = createScorePanel();
        add(prevScorePanel);
        add(Box.createVerticalStrut(10));
        add(nextScorePanel);

        add(Box.createVerticalStrut(15));
        add(createSeparator());
        add(Box.createVerticalStrut(15));

        // Pairs section - show all pairs (scrollable)
        add(createSectionLabel("PAIRS"));
        topPairsArea = createTextArea(10);
        JScrollPane pairsScroll = new JScrollPane(topPairsArea);
        pairsScroll.setPreferredSize(new Dimension(430, 250));  // Much wider
        pairsScroll.setMaximumSize(new Dimension(430, 250));
        add(pairsScroll);

        add(Box.createVerticalStrut(15));

        // Players section - show all players (scrollable)
        add(createSectionLabel("PLAYERS"));
        topPlayersArea = createTextArea(10);
        JScrollPane playersScroll = new JScrollPane(topPlayersArea);
        playersScroll.setPreferredSize(new Dimension(430, 250));  // Much wider
        playersScroll.setMaximumSize(new Dimension(430, 250));
        add(playersScroll);

        add(Box.createVerticalGlue());
    }

    private JLabel createSectionLabel(String text) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("SansSerif", Font.BOLD, 14));
        label.setAlignmentX(Component.LEFT_ALIGNMENT);
        return label;
    }

    private JLabel createDataLabel(String text) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("SansSerif", Font.PLAIN, 12));
        label.setAlignmentX(Component.LEFT_ALIGNMENT);
        return label;
    }

    private JPanel createScorePanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY, 1));
        panel.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.setMaximumSize(new Dimension(430, 80));  // Match new width
        return panel;
    }

    private JTextArea createTextArea(int rows) {
        JTextArea area = new JTextArea(rows, 20);
        area.setEditable(false);
        area.setFont(new Font("Monospaced", Font.PLAIN, 11));  // Back to 11 with more space
        return area;
    }

    private JSeparator createSeparator() {
        JSeparator sep = new JSeparator(SwingConstants.HORIZONTAL);
        sep.setMaximumSize(new Dimension(430, 1));  // Match new width
        return sep;
    }

    /**
     * Update panel with current graph data
     */
    public void updateStats(Graph graph, String club, String season, 
                           DynamicScoreData prevTransition, DynamicScoreData nextTransition) {
        // Basic info
        clubLabel.setText("Club: " + formatClubName(club));
        seasonLabel.setText("Season: " + formatSeason(season));
        
        int playerCount = graph.getNodeCount();
        int edgeCount = graph.getEdgeCount();
        double density = calculateDensity(playerCount, edgeCount);
        
        playersLabel.setText("Players: " + playerCount);
        edgesLabel.setText("Pairs: " + edgeCount);
        densityLabel.setText(String.format("Density: %.2f", density));

        // DynamicScore
        updateScorePanel(prevScorePanel, prevTransition, true);
        updateScorePanel(nextScorePanel, nextTransition, false);

        // Top pairs
        updateTopPairs(graph);

        // Top players
        updateTopPlayers(graph);
    }

    private void updateScorePanel(JPanel panel, DynamicScoreData data, boolean isPrev) {
        panel.removeAll();
        panel.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY, 1));
        panel.setAlignmentX(Component.LEFT_ALIGNMENT);
        
        if (data == null) {
            JLabel label = new JLabel(isPrev ? "  No data (first season)" : "  No data (last season)");
            label.setFont(new Font("SansSerif", Font.ITALIC, 11));
            label.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));
            panel.add(label);
        } else {
            String transition = formatSeason(data.getSeasonFrom()) + " → " + formatSeason(data.getSeasonTo());
            JLabel titleLabel = new JLabel("  " + transition);
            titleLabel.setFont(new Font("SansSerif", Font.BOLD, 11));
            titleLabel.setBorder(BorderFactory.createEmptyBorder(5, 5, 2, 5));
            
            JLabel vLabel = new JLabel(String.format("  V-Score: %.3f", data.getVScore()));
            vLabel.setFont(new Font("SansSerif", Font.PLAIN, 11));
            vLabel.setForeground(getScoreColor(data.getVScore()));
            vLabel.setBorder(BorderFactory.createEmptyBorder(2, 5, 2, 5));
            
            JLabel eLabel = new JLabel(String.format("  E-Score: %.3f", data.getEScore()));
            eLabel.setFont(new Font("SansSerif", Font.PLAIN, 11));
            eLabel.setForeground(getScoreColor(data.getEScore()));
            eLabel.setBorder(BorderFactory.createEmptyBorder(2, 5, 5, 5));
            
            panel.add(titleLabel);
            panel.add(vLabel);
            panel.add(eLabel);
        }
        
        panel.revalidate();
        panel.repaint();
    }

    private Color getScoreColor(double score) {
        if (score < 0.2) return new Color(0, 150, 0);      // Green
        if (score < 0.4) return new Color(200, 150, 0);    // Yellow
        if (score < 0.6) return new Color(255, 140, 0);    // Orange
        return new Color(200, 0, 0);                       // Red
    }

    private void updateTopPairs(Graph graph) {
        // Get all edges sorted by weight
        List<Edge> edges = new ArrayList<>();
        graph.edges().forEach(edges::add);
        
        edges.sort((e1, e2) -> {
            int w1 = e1.getAttribute("weight", Integer.class);
            int w2 = e2.getAttribute("weight", Integer.class);
            return Integer.compare(w2, w1); // Descending
        });

        StringBuilder sb = new StringBuilder();
        int count = Math.min(30, edges.size());  // Show up to 30 pairs
        for (int i = 0; i < count; i++) {
            Edge e = edges.get(i);
            int weight = e.getAttribute("weight", Integer.class);
            sb.append(String.format("%d. %s - %s (%d)\n", 
                i + 1,
                e.getNode0().getId(),
                e.getNode1().getId(),
                weight));
        }
        
        topPairsArea.setText(sb.toString());
    }

    private void updateTopPlayers(Graph graph) {
        // Get all nodes sorted by matches
        List<Node> nodes = new ArrayList<>();
        graph.nodes().forEach(nodes::add);
        
        nodes.sort((n1, n2) -> {
            int m1 = n1.getAttribute("matches", Integer.class);
            int m2 = n2.getAttribute("matches", Integer.class);
            return Integer.compare(m2, m1); // Descending
        });

        StringBuilder sb = new StringBuilder();
        // Show all players
        for (int i = 0; i < nodes.size(); i++) {
            Node n = nodes.get(i);
            int matches = n.getAttribute("matches", Integer.class);
            sb.append(String.format("%d. %s (%d)\n", 
                i + 1,
                n.getId(),
                matches));
        }
        
        topPlayersArea.setText(sb.toString());
    }

    private double calculateDensity(int nodes, int edges) {
        if (nodes <= 1) return 0.0;
        int maxEdges = nodes * (nodes - 1) / 2;
        return (double) edges / maxEdges;
    }

    private String formatClubName(String club) {
        return club.replace("_", " ").toUpperCase();
    }

    private String formatSeason(String season) {
        return season.replace("_", "/");
    }
}
