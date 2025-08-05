SELECT 
	usageEvents.pkgId,
  datetime(usageEvents.timeStamp / 1000, 'unixepoch') AS timestamps, --UTC
  --datetime(usageEvents.timeStamp / 1000, 'unixepoch', '-5 hours') AS timestamps, --CDT (UTC-5:00)
  foundPackages.name, 
  usageEvents.eventType,
	CASE
		when usageEvents.eventType=0 THEN 'NONE'
		when usageEvents.eventType=1 THEN 'ACTIVITY_RESUMED'
		when usageEvents.eventType=2 THEN 'ACTIVITY_PAUSED'
		when usageEvents.eventType=5 THEN 'CONFIGURATION_CHANGE'
		when usageEvents.eventType=7 THEN 'USER_INTERACTION'
		when usageEvents.eventType=8 THEN 'SHORTCUT_INVOCATION'
		when usageEvents.eventType=11 THEN 'STANDBY_BUCKET_CHANGED'
		when usageEvents.eventType=12 THEN 'NOTIFICATION'
		when usageEvents.eventType=15 THEN 'SCREEN_INTERACTIVE'
		when usageEvents.eventType=16 THEN 'SCREEN_NON_INTERACTIVE'
		when usageEvents.eventType=17 THEN 'KEYGUARD_SHOWN'
		when usageEvents.eventType=18 THEN 'KEYGUARD_HIDDEN (DEVICE UNLOCK)'
		when usageEvents.eventType=19 THEN 'FOREGROUND_SERVICE START'
		when usageEvents.eventType=20 THEN 'FOREGROUND_SERVICE_STOP'
		when usageEvents.eventType=23 THEN 'ACTIVITY_STOPPED'
		when usageEvents.eventType=26 THEN 'DEVICE_SHUTDOWN'
		when usageEvents.eventType=27 THEN 'DEVICE_STARTUP'
  	ELSE CAST(usageEvents.eventType AS TEXT)
  END AS eventTypeReadable
FROM usageEvents
INNER JOIN foundPackages ON usageEvents.pkgId = foundPackages.pkgId
ORDER BY eventType;