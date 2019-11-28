SELECT p.title, COUNT(CASE WHEN n.status = "Open" THEN 1 ELSE NULL END) as Open,
COUNT(CASE WHEN n.status = "Closed" THEN 1 ELSE NULL END) as Closed,
COUNT(CASE WHEN n.status = "In Progress" THEN 1 ELSE NULL END) as In_Progress,
COUNT(CASE WHEN n.status = "Resolved" THEN 1 ELSE NULL END) as Resolved FROM projects p
LEFT JOIN notes n ON n.project_id = p.id
WHERE p.user_id = 1
GROUP BY p.title

SELECT title, project_id, COUNT(*) as `count` FROM notes GROUP BY project_id, status ORDER BY project_id, status;