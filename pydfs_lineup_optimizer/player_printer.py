from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pydfs_lineup_optimizer.player import Player

class BasePlayerPrinter:
    def print_player(self, player: 'LineupPlayer') -> str:
        raise NotImplementedError


class PlayerPrinter(BasePlayerPrinter):
    OUTPUT_FORMAT = '{name:<30}{team:<3} {positions:<6}{exp:3.0f}% {id:<30}'

    #def _print_game_info(self, player: 'LineupPlayer') -> str:
     #   game_info = player.game_info
      #  if game_info:
       #     return '%s@%s' % (game_info.away_team, game_info.home_team)
        #return ''

    def _print_player(self, player: 'LineupPlayer', total_lineups: int) -> str:
        return self.OUTPUT_FORMAT.format(
            name='%s%s' % (player.full_name, '(%s)' % player.roster_order if player.roster_order else ''),
            
            positions='/'.join(player.original_positions), 
            team=player.team,
            exp=100*(player.lineup_count*1.0)/total_lineups,
            id=player.id,
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

    def print_player_ownership(self, players, total_lineups):
        player_ownerships = []
        players.sort(key=lambda x: (x.team, x.roster_order))
        for player in players:
            if (player.lineup_count > 0):
                print(self._print_player(player, total_lineups))
        


#class IndividualSportLineupPrinter(PlayerPrinter):
 #   OUTPUT_FORMAT = '{index:>2}. {lineup_position:<5} {name:<30}{fppg:<15}{salary:<10}\n'


#class DraftKingTiersLineupPrinter(LineupPrinter):
 #   OUTPUT_FORMAT = '{index:>2}. {lineup_position:<5} {name:<30}{fppg:<15}\n'
