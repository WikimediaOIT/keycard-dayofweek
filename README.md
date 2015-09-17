# keycard-dayofweek

This script it meant to read in CSV files from an AllGuard security system
and do an analysis of what day of week individuals come in...

This can help with office space planning.

example input format:

"Gen Time","Seq ID","Type","Status","P","Reader","Site","Card Number","Account","Name","Operator","Message"
"6/1/2015 12:48:00 AM","4395401","Card","Valid Card","79","Lobby","Readers","50783","NCI","Cat, Garfield","Allguard",""
"6/1/2015 6:43:00 AM","4395781","Card","Valid Card","79","Hall","Readers","8131","NCI","Dog, Snoopy ","Allguard",""
"6/1/2015 6:46:00 AM","4395782","Card","Valid Card","79","Stairs","Readers","8131","NCI","Mouse, Jerry ","Allguard",""


example output  (lastname, firstname, mondays, tuesdays, ..., total)
Mouse, Jerry, 8, 10, 12, 11, 7, 0, 0, 48
Dog, Snoopy, 0, 1, 0, 0, 1, 0, 0, 2
Cat, Garfield, 2, 6, 2, 6, 1, 0, 0, 17
