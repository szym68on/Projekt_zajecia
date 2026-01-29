import java.util.List;
import com.google.gson.annotations.SerializedName;

/**
 * Model for DynamicScore data between two consecutive seasons
 */
public class DynamicScoreData {
    private String club;
    
    @SerializedName("season_from")
    private String seasonFrom;
    
    @SerializedName("season_to")
    private String seasonTo;
    
    @SerializedName("v_score")
    private double vScore;
    
    @SerializedName("e_score")
    private double eScore;
    
    private Stats stats;
    
    @SerializedName("players_left")
    private List<PlayerChange> playersLeft;
    
    @SerializedName("players_joined")
    private List<PlayerChange> playersJoined;
    
    @SerializedName("edges_lost")
    private List<EdgeChange> edgesLost;
    
    @SerializedName("edges_gained")
    private List<EdgeChange> edgesGained;

    // Inner classes for nested JSON structure
    public static class Stats {
        @SerializedName("total_players_t")
        private int totalPlayersT;
        
        @SerializedName("total_players_t1")
        private int totalPlayersT1;
        
        @SerializedName("total_edges_t")
        private int totalEdgesT;
        
        @SerializedName("total_edges_t1")
        private int totalEdgesT1;

        public int getTotalPlayersT() { return totalPlayersT; }
        public int getTotalPlayersT1() { return totalPlayersT1; }
        public int getTotalEdgesT() { return totalEdgesT; }
        public int getTotalEdgesT1() { return totalEdgesT1; }
    }

    public static class PlayerChange {
        private String name;
        private int matches;

        public String getName() { return name; }
        public int getMatches() { return matches; }
    }

    public static class EdgeChange {
        private String player1;
        private String player2;
        private int weight;

        public String getPlayer1() { return player1; }
        public String getPlayer2() { return player2; }
        public int getWeight() { return weight; }
    }

    // Getters
    public String getClub() { return club; }
    public String getSeasonFrom() { return seasonFrom; }
    public String getSeasonTo() { return seasonTo; }
    public double getVScore() { return vScore; }
    public double getEScore() { return eScore; }
    public Stats getStats() { return stats; }
    public List<PlayerChange> getPlayersLeft() { return playersLeft; }
    public List<PlayerChange> getPlayersJoined() { return playersJoined; }
    public List<EdgeChange> getEdgesLost() { return edgesLost; }
    public List<EdgeChange> getEdgesGained() { return edgesGained; }
}
