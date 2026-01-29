import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Type;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

/**
 * Loads DynamicScore data from JSON files
 */
public class DynamicScoreLoader {
    private static final String DYNAMIC_SCORES_DIR = "../dynamic_scores";
    private Map<String, List<DynamicScoreData>> clubData;
    private Gson gson;

    public DynamicScoreLoader() {
        gson = new Gson();
        clubData = new HashMap<>();
        loadAllClubData();
    }

    /**
     * Load all club JSON files
     */
    private void loadAllClubData() {
        String[] clubs = {
            "athletic_bilbao",
            "atletico_madryt", 
            "fc_barcelona",
            "real_madryt",
            "villarreal_cf"
        };

        for (String club : clubs) {
            String filename = String.format("%s/%s_dynamic_scores.json", DYNAMIC_SCORES_DIR, club);
            List<DynamicScoreData> data = loadClubFile(filename);
            if (data != null) {
                clubData.put(club, data);
            }
        }

        System.out.println("Loaded DynamicScore data for " + clubData.size() + " clubs");
    }

    /**
     * Load a single club JSON file
     */
    private List<DynamicScoreData> loadClubFile(String filename) {
        try (FileReader reader = new FileReader(filename)) {
            Type listType = new TypeToken<List<DynamicScoreData>>(){}.getType();
            List<DynamicScoreData> data = gson.fromJson(reader, listType);
            System.out.println("Loaded " + filename + ": " + data.size() + " transitions");
            return data;
        } catch (IOException e) {
            System.err.println("Could not load " + filename + ": " + e.getMessage());
            return null;
        }
    }

    /**
     * Get DynamicScore data for transition from season to next season
     * Returns null if not found
     */
    public DynamicScoreData getTransition(String club, String season) {
        List<DynamicScoreData> transitions = clubData.get(club);
        if (transitions == null) return null;

        for (DynamicScoreData data : transitions) {
            if (data.getSeasonFrom().equals(season)) {
                return data;
            }
        }
        return null;
    }

    /**
     * Get DynamicScore data for transition TO current season (from previous)
     * Returns null if not found
     */
    public DynamicScoreData getTransitionTo(String club, String season) {
        List<DynamicScoreData> transitions = clubData.get(club);
        if (transitions == null) return null;

        for (DynamicScoreData data : transitions) {
            if (data.getSeasonTo().equals(season)) {
                return data;
            }
        }
        return null;
    }

    /**
     * Get all available clubs
     */
    public Set<String> getAvailableClubs() {
        return clubData.keySet();
    }

    /**
     * Check if data exists
     */
    public boolean hasData() {
        return !clubData.isEmpty();
    }

    /**
     * Get all transitions for a specific club
     */
    public List<DynamicScoreData> getClubTransitions(String club) {
        return clubData.get(club);
    }
}
