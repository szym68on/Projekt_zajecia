import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import javax.swing.*;
import java.awt.*;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Timeline window showing DynamicScore evolution over seasons
 */
public class TimelineWindow extends JFrame {
    private String club;
    private DynamicScoreLoader scoreLoader;

    public TimelineWindow(String club, DynamicScoreLoader scoreLoader) {
        super("Timeline - " + club.replace("_", " ").toUpperCase() + " (2005-2025)");
        this.club = club;
        this.scoreLoader = scoreLoader;

        setLayout(new BorderLayout());
        
        // Create chart
        JFreeChart chart = createTimelineChart();
        ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new Dimension(1200, 700));
        
        add(chartPanel, BorderLayout.CENTER);
        
        // Bottom panel with statistics
        JPanel bottomPanel = createBottomPanel();
        add(bottomPanel, BorderLayout.SOUTH);

        pack();
        setLocationRelativeTo(null);
    }

    private JFreeChart createTimelineChart() {
        // Create dataset
        XYSeriesCollection dataset = new XYSeriesCollection();
        
        XYSeries vScoreSeries = new XYSeries("V-Score (Players)");
        XYSeries eScoreSeries = new XYSeries("E-Score (Pairs)");
        
        // Get all transitions for this club
        List<DynamicScoreData> transitions = getClubTransitions();
        
        if (transitions == null || transitions.isEmpty()) {
            // Empty chart if no data
            vScoreSeries.add(0, 0);
            eScoreSeries.add(0, 0);
        } else {
            // Add data points - use season end year as X coordinate
            for (DynamicScoreData data : transitions) {
                int year = extractEndYear(data.getSeasonFrom());
                vScoreSeries.add(year, data.getVScore());
                eScoreSeries.add(year, data.getEScore());
            }
        }
        
        dataset.addSeries(vScoreSeries);
        dataset.addSeries(eScoreSeries);

        // Create chart
        JFreeChart chart = ChartFactory.createXYLineChart(
            "Team Evolution - " + formatClubName(club),
            "Year",
            "DynamicScore",
            dataset,
            PlotOrientation.VERTICAL,
            true,  // legend
            true,  // tooltips
            false  // urls
        );

        // Customize chart appearance
        XYPlot plot = chart.getXYPlot();
        plot.setBackgroundPaint(Color.WHITE);
        plot.setDomainGridlinePaint(Color.LIGHT_GRAY);
        plot.setRangeGridlinePaint(Color.LIGHT_GRAY);

        // Customize renderer
        XYLineAndShapeRenderer renderer = new XYLineAndShapeRenderer();
        
        // V-Score line - blue
        renderer.setSeriesPaint(0, new Color(70, 130, 180));  // Steel blue
        renderer.setSeriesStroke(0, new BasicStroke(3.0f));
        renderer.setSeriesShapesVisible(0, true);
        
        // E-Score line - orange
        renderer.setSeriesPaint(1, new Color(255, 140, 0));   // Dark orange
        renderer.setSeriesStroke(1, new BasicStroke(3.0f));
        renderer.setSeriesShapesVisible(1, true);
        
        plot.setRenderer(renderer);

        return chart;
    }

    private JPanel createBottomPanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Get transitions
        List<DynamicScoreData> transitions = getClubTransitions();
        
        if (transitions == null || transitions.isEmpty()) {
            JLabel label = new JLabel("No data available");
            label.setAlignmentX(Component.CENTER_ALIGNMENT);
            panel.add(label);
            return panel;
        }

        // Title
        JLabel titleLabel = new JLabel("BIGGEST CHANGES");
        titleLabel.setFont(new Font("SansSerif", Font.BOLD, 14));
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        panel.add(titleLabel);
        panel.add(Box.createVerticalStrut(10));

        // Create table-like display
        JPanel tablePanel = new JPanel(new GridLayout(0, 3, 20, 5));
        
        // Headers
        tablePanel.add(createHeaderLabel("Season"));
        tablePanel.add(createHeaderLabel("V-Score"));
        tablePanel.add(createHeaderLabel("E-Score"));

        // Get top 5 changes by E-Score (more interesting)
        List<DynamicScoreData> topChanges = transitions.stream()
            .sorted((a, b) -> Double.compare(b.getEScore(), a.getEScore()))
            .limit(5)
            .collect(Collectors.toList());

        // Display top changes
        for (DynamicScoreData data : topChanges) {
            tablePanel.add(createDataLabel(formatSeason(data.getSeasonFrom()) + " → " + formatSeason(data.getSeasonTo())));
            tablePanel.add(createScoreLabel(data.getVScore()));
            tablePanel.add(createScoreLabel(data.getEScore()));
        }

        panel.add(tablePanel);

        return panel;
    }

    private JLabel createHeaderLabel(String text) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("SansSerif", Font.BOLD, 12));
        return label;
    }

    private JLabel createDataLabel(String text) {
        JLabel label = new JLabel(text);
        label.setFont(new Font("SansSerif", Font.PLAIN, 11));
        return label;
    }

    private JLabel createScoreLabel(double score) {
        JLabel label = new JLabel(String.format("%.3f", score));
        label.setFont(new Font("SansSerif", Font.PLAIN, 11));
        label.setForeground(getScoreColor(score));
        return label;
    }

    private Color getScoreColor(double score) {
        if (score < 0.2) return new Color(0, 150, 0);      // Green
        if (score < 0.4) return new Color(200, 150, 0);    // Yellow
        if (score < 0.6) return new Color(255, 140, 0);    // Orange
        return new Color(200, 0, 0);                       // Red
    }

    private List<DynamicScoreData> getClubTransitions() {
        return scoreLoader.getClubTransitions(club);
    }

    private int extractEndYear(String season) {
        // Extract end year from season format "2015_2016" -> 2016
        String[] parts = season.split("_");
        if (parts.length == 2) {
            return Integer.parseInt(parts[1]);
        }
        return 2005;
    }

    private String formatSeason(String season) {
        return season.replace("_", "/");
    }

    private String formatClubName(String club) {
        return club.replace("_", " ").toUpperCase();
    }
}