#from pulp.solvers import PULP_CBC_CMD
import json
from pydfs_lineup_optimizer import get_optimizer, Site, Sport
from pydfs_lineup_optimizer.player_printer import BasePlayerPrinter, PlayerPrinter 
from pydfs_lineup_optimizer.stacks import BaseGroup, TeamStack, PositionsStack, BaseStack, Stack

from pydfs_lineup_optimizer.exceptions import LineupOptimizerException
#from pydfs_lineup_optimizer.solvers.pulp_solver import PuLPSolver


#class CustomPuLPSolver(PuLPSolver):
 #   LP_SOLVER = PULP_CBC_CMD(threads=8, options=['preprocess off'])

def _mapPlayer (this, name, mapping) -> str:
    mappedName = mapping.get(name)
    if mappedName:
        return mappedName
    else:
        return name
        
        
    
slateConfigJson = """
{ 
    "site":"FANDUEL",
    "sport":"FOOTBALL",
    "file":"FanDuel-NFL-2020-11-08-51377-lineup-upload-template.csv",
    "QBS": [
        {"name":"Russell Wilson","exposure":0.15}, 
        {"name":"Kirk Cousins","exposure":0.05 },
        {"name":"Deshaun Watson","exposure":0.15},
        {"name":"Justin Herbert","exposure":0.15},
        {"name":"Derek Carr","exposure":0.12},
        {"name":"Kyler Murray","exposure":0.08},
        {"name":"Matt Ryan","exposure":0.10},
        {"name":"Drew Lock","exposure":0.05},
        {"name":"Josh Allen","exposure":0.12},
        {"name":"Lamar Jackson","exposure":0.1}
        ],
    "FLEX": [
        {"name":"David Montgomery", "exposure":0.01},
        {"name":"Dalvin Cook","exposure":0.40},
        {"name":"James Conner","exposure":0.40},
        {"name":"James Robinson","exposure":0.08},
        {"name":"Chase Edmonds","exposure":0.10},
        {"name":"Christian McCaffrey","exposure":0.10, "minExposure":0.03},
        {"name":"Derrick Henry","exposure":0.20},
        {"name":"Todd Gurley II","exposure":0.01},
        {"name":"Zack Moss","exposure":0.0},
        {"name":"Devin Singletary","exposure":0},
        {"name":"David Johnson", "exposure":0.05},
        {"name":"Le'Veon Bell","exposure":0.01},
        {"name":"Clyde Edwards-Helaire","exposure":0.03},
        {"name":"Nyheim Hines","exposure":0.0},
        {"name":"Jordan Wilkins","exposure":0.01},
        {"name":"Jonathan Taylor","exposure":0.01},
        {"name":"Gus Edwards","exposure":0},
        {"name":"J.K. Dobbins","exposure":0.03},
        {"name":"Adrian Peterson","exposure":0.01},
        {"name":"Royce Freeman","exposure":0},
                
    
    
        {"name":"Tyler Lockett","exposure":0.50},
        {"name":"Julio Jones", "exposure":0.40},
        {"name":"Keenan Allen","exposure":0.35},
        {"name":"Brandin Cooks","exposure":0.20,"minExposure":0.10},
        {"name":"Christian Kirk","exposure":0.15, "minExposure":0.08},
        {"name":"Cordarrelle Patterson","exposure":0},
        {"name":"Darnell Mooney","exposure":0.05, "minExposure":0.05},
        {"name":"Marquise Brown","exposure":0.15, "minExposure":0.08},
        {"name":"John Brown", "exposure":0.10},
        {"name":"Cole Beasley","exposure":0.05},
        {"name":"Isaiah McKenzie", "exposure":0.0},
        {"name":"Jerry Jeudy","exposure":0.10},
        {"name":"Tyreek Hill","exposure":0.10},
        {"name":"Henry Ruggs III","exposure":0.10, "minExposure":0.05},
        {"name":"Sterling Shepard", "exposure":0.10, "minExposure":0.05},
        {"name":"Larry Fitzgerald","exposure":0.0},
        {"name":"Andy Isabella","exposure":0.0},
        {"name":"Nelson Agholor","exposure":0.01},
        {"name":"Quintez Cehpus","exposure":0},
        
        
        
        {"name":"Logan Thomas","exposure":0.05}
    ]
    "FAFanDuelMapping": [
    {"Will Fuller":"Will Fuller V"},
    {"Todd Gurley":"Todd Gurley II"},
    {"Allen Robinson":"Allen Robinson II"},
    {"Melvin Gordon":"Melvin Gordon III"},
    {"Dwayne Haskins":"Dwayne Haskins Jr."},
    {"D.J. Chark":"DJ Chark Jr."},
    {"Marvin Jones":"Marvin Jones Jr."},
    {"Robert Griffin":"Robert Griffin III"},
    {"Henry Ruggs":"Henry Ruggs III"},
    {"Mark Ingram":"Mark Ingram II"},
    {"Wayne Gallman":"Wayne Gallman Jr."},
    {"Laviska Shenault":"Laviska Shenault Jr."}
    {"Willie Snead":"Willie Snead IV"},
    {"Benny Snell":"Benny Snell Jr."},
    {"Michael Pittman":"Michael Pittman Jr."},
    {"K.J. Hamler":"KJ Hamler"},
    {"Irv Smith":"Irv Smith Jr."},
    {"Steve Sims":"Steve Sims Jr."},
    {"Donald Parham":"Donald Parham Jr."}
    
    ]
}"""
    
slateConfig = json.loads(slateConfigJson)

optimizer = get_optimizer(slateConfig["site"], slateConfig["sport"])

optimizer.load_players_from_csv("CSVFiles/" + slateConfig["file"])

lineupsWanted = 150

for player in optimizer.players:
    if player.efficiency == 0:
        optimizer.remove_player(player)
    #if 'QB' in player.original_positions:
    #    optimizer.remove_player(player)
   # if 'RB' in player.original_positions:
    #    optimizer.remove_player(player)
     

        
for qb in slateConfig["QBS"]:
    print(qb)
    player = optimizer.get_player_by_name(_mapPlayer(qb["name"])
    player.max_exposure=qb["exposure"]
    player.projected_points = qb["projPoints"]
    optimizer.restore_player(player)
    
for flex in slateConfig["FLEX"]:
    player = optimizer.get_player_by_name(flex["name"])
    player.max_exposure=flex["exposure"]
    if "minExposure" in flex.keys():
        player.min_exposure=flex["minExposure"]
    #optimizer.restore_player(player)
    
for d in optimizer.players:
    if 'D' in player.original_positions:
        player.max_exposure = 15
   
    

#rbs = ['Alvin Kamara', 'Kareem Hunt', 'Gio Bernard', 'Justin Jackson', 'Joshua Kelley', 'Derrick Henry', 'Todd Gurley', 'Jamaal Williams','Ezekiel Elliott','Chris Carson', 'James Robinson','Antonio Gibson']
#for rb in rbs:
 #   player = optimizer.get_player_by_name(rb)
#    player.max_exposure=1.0/(len(rb)-1)
   # optimizer.restore_player(player)

optimizer.restrict_positions_for_same_team(('RB', 'RB'), ('QB', 'D'), ('TE','TE'), ('RB', 'WR'), ('RB', 'TE'),('QB','D'))
#optimizer.add_stack(TeamStack(3, for_positions=['QB', 'WR'], max_exposure=0.05, for_teams=['SEA','HOU'])) 
optimizer.add_stack(PositionsStack(['QB', ('WR', 'TE')], max_exposure=0.99, for_teams=['SEA','ARI', 'HOU','MIN','LAC','LV','ATL','DEN', 'BAL', 'BUF']))   
#optimizer.add_stack(PositionsStack(['QB', 'WR', 'WR'], max_exposure=0.10, for_teams=['SEA','HOU']))   
# stack 3 players with any of specified positions
optimizer.force_positions_for_opposing_team(('QB', 'WR'), ('RB', 'WR'))

optimizer.set_deviation(0.2,0.7)
lineups = optimizer.optimize(n=lineupsWanted, max_exposure=0.10, randomness=True)
#optimizer.print_statistic()
lineup_counter = 0;
try:
    for lineup in lineups:
        lineup_counter += 1
        print(lineup_counter)
        print(lineup)
        print(lineup.players)  # list of players
        print(lineup.fantasy_points_projection)
        print(lineup.salary_costs)
except LineupOptimizerException:
    print('Stopping at {} lineups'.format(lineup_counter))
optimizer.print_statistic()
optimizer.export("results.csv")

    
playerPrinter = PlayerPrinter() 
playerPrinter.print_player_ownership(optimizer.players, lineup_counter)



#playerMatcher = PlayerMatcherPrinter()
#playerMatcher.print_player_matches(optimizer.players, lineups)


