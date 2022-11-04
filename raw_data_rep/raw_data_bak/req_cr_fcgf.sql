USE PLCData_Lake_20221012
GO

DECLARE @NSerie AS INT = 22375847;

CREATE TABLE #LST_TRY
(SN INT, RowId_Deb INT , RowId_Fin INT)

CREATE TABLE #DATA
 (DateHeure Datetime
      ,ProgTest NVARCHAR(10)
      ,VersionProg SMALLINT
      ,VersionBanc NVARCHAR(10)
      ,CodeArticle NVARCHAR(8)
      ,NumSerie INT
      ,NumLot INT
      ,Conformite TINYINT
      ,NumSequence SMALLINT
      ,TeteControle TINYINT
      ,ValMini REAL
      ,Resultat REAL
      ,ValMaxi REAL
      ,Unite TINYINT
      ,Conforme TINYINT
      ,Operateur NVARCHAR(20)
      ,ROWID INT
	  )


INSERT INTO #LST_TRY
	SELECT DISTINCT DEB.NumSerie, DEB.MaxRow, FIN.MaxRow FROM 
	(SELECT NumSerie, MAX(ROWID) OVER (PARTITION BY NumSerie) AS MaxRow FROM [PLC1] AS A  
		WHERE NumSequence = (SELECT NumSequence FROM [PLCData_Lake_20221012].[dbo].[Tbl-Ref-Fab-Detail] 
								WHERE ProgTest = A.ProgTest 
								AND	VersionProg = A.VersionProg
								AND  OrdSeqAutomate = 1)
				AND NumSerie = @NSerie

	) AS DEB

	LEFT JOIN	(SELECT NumSerie, MAX(ROWID) OVER (PARTITION BY NumSerie) AS MaxRow  FROM [PLC1] WHERE NumSerie = @NSerie)  AS FIN
	ON FIN.NumSerie = DEB.NumSerie;

INSERT INTO #DATA
SELECT [DateHeure]
      ,[ProgTest]
      ,[VersionProg]
      ,[VersionBanc]
      ,(SELECT CodeArticle FROM [Tbl-Ref-BaseArticle] WHERE UDI = A.UDI) AS CodeArticle 
      ,[NumSerie]
      ,[NumLot]
      ,[Conformite]
      ,[NumSequence]
      ,[TeteControle]
      ,[ValMini]
      ,[Resultat]
      ,[ValMaxi]
      ,[Unite]
      ,[Conforme]
      ,[Operateur]
      ,[ROWID]
	  
	   FROM PLC1 AS A  WHERE ROWID BETWEEN (SELECT RowId_Deb FROM #LST_TRY where SN = A.NumSerie) AND (SELECT RowId_Fin FROM #LST_TRY where SN = A.NumSerie)
	   AND NumSerie = @NSerie;

SELECT BASE.NumSerie
,BASE.NumLot
,BASE.CodeArticle
,(SELECT Designation FROM [Tbl-Ref-BaseArticle] WHERE CodeArticle = #DATA.CodeArticle) As Designation
,BASE.ProgTest
,BASE.VersionProg
,#DATA.VersionBanc
,RFD.OrdreFCGF
,#DATA.ROWID
,#DATA.NumSequence
,#DATA.DateHeure
,RFD.Sequence
,(SELECT Valeur FROM [Tbl-Ref-Parametres] WHERE Type_Parametre = 'TeteControle' AND ID_Parametre = #DATA.TeteControle) AS T_CTRL
,#DATA.ValMini
,#DATA.Resultat
,#DATA.ValMaxi
,(SELECT Valeur FROM [Tbl-Ref-Parametres] WHERE Type_Parametre = 'Unité' AND ID_Parametre = #DATA.Unite) AS Unite
,IIF(#DATA.Conformite IS NULL, 'Non Conforme', (SELECT Valeur FROM [Tbl-Ref-Parametres] WHERE Type_Parametre = 'Statut' AND ID_Parametre = #DATA.Conformite)) AS Statut
,#DATA.Operateur
,(SELECT Valeur FROM [PLCData_Lake_20221012].[dbo].[Tbl-Ref-Parametres]
			WHERE [Type_Parametre] = 'Statut' 
			AND ID_Parametre = (IIF (
									(SELECT NumSequence FROM #DATA WHERE ROWID = (SELECT RowId_Fin FROM #LST_TRY )) = (select NumSequence FROM dbo.[Tbl-Ref-Fab-Detail] 
																							WHERE ProgTest = #DATA.ProgTest 
																							AND VersionProg = #DATA.VersionProg 
																							AND OrdSeqAutomate = ( SELECT DISTINCT MAX(OrdSeqAutomate) FROM dbo.[Tbl-Ref-Fab-Detail]
																													WHERE ProgTest = #DATA.ProgTest 
																													AND VersionProg = #DATA.VersionProg )
																												
																												)

								, (SELECT Conforme FROM #DATA WHERE ROWID = (SELECT RowId_Fin FROM #LST_TRY ))
								, 0) )) AS Conf_Globale
,RFL.Titre_FCGF
,RFL.Verificateur
,CONVERT(NVARCHAR, RFL.Date_Verif, 103)  AS Date_Verif
,RFL.Approbateur
,CONVERT(NVARCHAR, RFL.Date_Appr, 103)  AS Date_Appr
,CONVERT(NVARCHAR, RFL.Date_Application, 103)  AS Date_Application
,RFL.Visa
,CONVERT(NVARCHAR, #DATA.DateHeure, 103) AS DateValid
 FROM 
(SELECT DISTINCT NumSerie, NumLot, CodeArticle, ProgTest, VersionProg FROM #DATA) AS BASE
LEFT JOIN (SELECT * FROM [Tbl-Ref-Fab-Detail] WHERE FCGF = 1) AS RFD
ON BASE.ProgTest = RFD.ProgTest AND BASE.VersionProg = RFD.VersionProg
LEFT JOIN #DATA ON #DATA.NumSerie = BASE.NumSerie AND #DATA.NumSequence = RFD.NumSequence
LEFT JOIN [PLCData_Lake_20221012].[dbo].[Tbl-Ref-Fab-Liste] AS RFL
ON RFL.CodeArticle = BASE.CodeArticle AND RFL.ProgTest = BASE.ProgTest AND RFL.VersionProg = BASE.VersionProg
WHERE BASE.NumSerie = @NSerie
ORDER BY BASE.NumSerie, RFD.OrdreFCGF ASC



DROP TABLE #LST_TRY, #DATA



