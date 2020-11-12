from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pydfs_lineup_optimizer.player import Player

class BasePlayerMatcherPrinter:
    def print_playerMatch(self, player: 'LineupPlayer') -> str:
        raise NotImplementedError


class PlayerMatcherPrinter(BasePlayerMatcherPrinter):
    OUTPUT_FORMAT = '{name1:<30} {name2:<30} {freq:3.0f}%'

    #def _print_game_info(self, player: 'LineupPlayer') -> str:
     #   game_info = player.game_info
      #  if game_info:
       #     return '%s@%s' % (game_info.away_team, game_info.home_team)
        #return ''

    def _print_player(self, player1: 'LineupPlayer', player2: 'LineupPlayer', frequency: float) -> str:
        return self.OUTPUT_FORMAT.format(
            name1='%s%s' % (player1.full_name, '(%s)'),
            name2='%s' % (player2.full_name, '(%s)'),
            freq=frequency,
       )

    def _print_footer(self, lineup: 'Lineup') -> str:
        original_projection = lineup.fantasy_points_projection
        actual_projection = lineup.actual_fantasy_points_projection
        footer = 'Fantasy Points %.2f%s\n' % (
            original_projection, '(%.2f)' % actual_projection if actual_projection != original_projection else '')
        if lineup.salary_costs:
            footer += 'Salary %.2f\n' % lineup.salary_costs
        ownerships = [player.projected_ownership for player in lineup if player.projected_ownership]
        if ownerships:
            footer += 'Average Ownership %.1f%%\n' % (sum(ownerships) * 100 / len(ownerships))
        return footer

    def print_player(self, player):
        if (player.lineup_count > 0):
            return self._print_player(player) + '\n'
        return ''

    def print_player_matches(self, players, lineups):
        players.sort(key=lambda x: (x.team, x.roster_order))
        playerMatches = []
        for player in players:
            if (player.lineup_count > 0):
                playerMatches[player.name] = []
                for lineup in lineups:
                    for lp in lineup.players:
                        if lp.name == player.name:
                            continue                        
                        playerMatches[player.name].append(lp.name)
        for p in playerMatches:
                
                         
        print(self._print_player(player1, player2, (1.0*matches)/player.lineup_count ))
        


#class IndividualSportLineupPrinter(PlayerPrinter):
 #   OUTPUT_FORMAT = '{index:>2}. {lineup_position:<5} {name:<30}{fppg:<15}{salary:<10}\n'


#class DraftKingTiersLineupPrinter(LineupPrinter):
 #   OUTPUT_FORMAT = '{index:>2}. {lineup_position:<5} {name:<30}{fppg:<15}\n'
