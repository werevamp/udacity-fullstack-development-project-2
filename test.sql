SELECT players.id, players.name, coalesce(winners.wins, 0), coalesce(matches_amount.matches, 0)
FROM players
LEFT JOIN (
	SELECT winner, coalesce(count(winner), 0) AS wins
	FROM matches
	GROUP BY winner
) AS winners
ON players.id = winners.winner
LEFT JOIN (
	SELECT players.id, coalesce(count(players.id), 0) AS matches
	FROM players
	JOIN matches
	ON players.id = matches.winner
		OR players.id = matches.loser
	GROUP BY players.id
) AS matches_amount
ON players.id = matches_amount.id
ORDER BY winners.wins DESC NULLS LAST;
