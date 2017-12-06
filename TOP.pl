#!usr/bin/perl
use warnings; use strict;
use LWP::Simple;


################################ 
###### daily report data
################################ 
=header
my $yearstart = 106;
my $yearend = 106;
my $monthstart = 1;
my $monthend = 12;
my $daystart = 2;
my $dayend = 31;
my @input_4;

print "\n ~~~~ TOP => Python daily ~~~~ \n\n";

for (my $year = $yearstart; $year <= $yearend; $year++){
	for (my $month = $monthstart; $month <= $monthend; $month++){
        for (my $day = $daystart; $day <= $dayend; $day++){
            my $a = 12, $b = 12;
            if ($month>=10){
				$a = " $month ";
				$a =~ s/ //g;
			}else{
				$a = " 0 $month ";
				$a =~ s/ //g;
            }
            if ($day>=10){
				$b = " $day ";
				$b =~ s/ //g;
			}else{
				$b = " 0 $day ";
				$b =~ s/ //g;                  
            }
            system "python daily_report.py $year $a $b";
        };
    };
};
=cut


################################ 
###### monthly report data
################################ 
my $yearstart = 106;
my $yearend = 106;
my $monthstart = 1;
my $monthend = 12;

print "\n ~~~~ TOP => Python monthly ~~~~ \n\n";
print " ~~~~ Year from $yearstart to $yearend ~~~~ \n";
print " ~~~~ Month from $monthstart to $monthend ~~~~ \n\n";

for (my $year = $yearstart; $year <= $yearend; $year++){
	for (my $month = $monthstart; $month <= $monthend; $month++){

        system "python monthly_report.py $year $month";
        #system "python monthly_report.py 106 03";
        #system "python monthly_report.py 106 04";
        #system "python monthly_report.py 106 05";
    };
};














=header
print "\n ~~~~ TOP => Python season ~~~~ \n\n";

system "python season_report.py 105 01 1";
system "python season_report.py 105 02 1";
system "python season_report.py 105 03 1";
system "python season_report.py 105 04 1";
=cut


#system "perl GetStockNumber.pl";

################################ 
###### daily : skill
################################ 
#system "perl History_tse.pl $yearstart $yearend $monthstart $monthend"; 

################################ 
##### daily : acredit foreign netbuy zhuli
################################ 
#system "perl HistoryBasic_2.pl $yearstart $yearend $monthstart $monthend"; 

################################ 
##### month : asale
################################ 
#system "perl HistoryBasic_3.pl $yearstart $yearend"; 

################################ 
##### year : dividend finicial 
##### season : balance income
################################ 
#system "perl HistoryBasic.pl";

#system "perl Hash.pl";

print "\n ~~~~ TOP => All works have been done! ~~~~ \n\n";

#After Hash.pl
=header 
~acredit~
日期 資餘 資增減 券餘 券增減 使用率 券資比 資券抵

~foreign~
日期 持股比率 持有張數 當日增減

~netbuy~
日期 投信 自營商 外資

~zhuli~
日期 主力庫存張數 增減張數

~skill~
日期 成交股數 成交金額 開盤價 最高價 最低價 收盤價 漲跌價差 成交筆數

~asale~
     營業額(仟元)                                               累計營業額(仟元)
年月 當月營收 上月營收 月營收增減 前一年同月營收 前一年同月增減	當年累計營收 前一年同期累計 前一年同期增減

~balance~
日期 流動比 資產總計 負債比 股東權益 股本(仟) 原始淨值

~income~
日期	營收(仟元)	營業毛利率	營業利益率	稅前純益率	稅後純益率	稅後EPS

~dividend~
            股票股利(股)                                                      現金股利(元)
股東會日期 盈餘配股(元/股) 公積配股(元/股) 除權交易日 (員工紅利)配股總張數 股東股利(元/股) 除息交易日 員工紅利總金額(仟元) 董監酬勞(仟元)

~finicial~
年度 營業毛利率 營業利益率 稅後淨利率 流動比率 速動比率 負債比率 利息保障倍數 每股淨值 應收帳款 週轉天數 股東權益報酬率 稅後EPS
=cut
