<?php
//IRIS  Rutgers Civil and Environmental Engineering, 2/27/2017
require 'YahooFinance.php';
$yf = new YahooFinance;

class U_Yahoo{

    private function file_get_contents_curl($url) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_HEADER, 0);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

        curl_setopt($ch, CURLOPT_URL, $url);

        $data = curl_exec($ch);
        curl_close($ch);

        return $data;
    }

    //return the history quote from the simbol, default begin date is 90 day ago, the default end is today
    public function getHistoryQuote_day($symbol, $begin = 90, $end = 0){
        if(!$begin && !$end)
            $begin = $end = 0;

        $begin = Date('Y-m-d', strtotime("-{$begin} days"));
        $end = Date('Y-m-d', strtotime("-{$end} days"));
        $url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22$symbol%22%20and%20startDate%20%3D%20%22$begin%22%20and%20endDate%20%3D%20%22$end%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=";
        $jason_obj = json_decode( $this->file_get_contents_curl($url) );
        return $jason_obj->query->results->quote;
    }


    //return the history quote from the simbol, default begin date is 90 day ago, the default end is today
    public function getHistoryQuote_min($symbol, $begin = 90, $end = 0){
        if(!$begin && !$end)
            $begin = $end = 0;
        $begin = Date('Y-m-d', strtotime("-{$begin} days"));
        $end = Date('Y-m-d', strtotime("-{$end} days"));
        $url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22$symbol%22%20and%20startDate%20%3D%20%22$begin%22%20and%20endDate%20%3D%20%22$end%22&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=";
        $jason_obj = json_decode( $this->file_get_contents_curl($url) );
        return $jason_obj->query->results->quote;
    }
    //return not just the quote but others informations too
    public function getCurrentData($symbol){
        $is_array = is_array($symbol);

        $imp_symbol = ($is_array)? implode('%22%2C%22', $symbol) : $symbol;

        $url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20where%20symbol%20in%20(%22$imp_symbol%22)&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=";
        $jason_obj = json_decode( $this->file_get_contents_curl($url) );

        $result = $jason_obj->query->results->quote;

        return (is_array($symbol) and (count($symbol) == 1))? [$result] : $result;
    }

    //return all quotes from the param $symbol passed, if symbol is array, it will return other array indexed by the symbols
    public function getCurrentQuote($symbol){
        if(is_array($symbol)){
            $symbol = empty($symbol)? ['GOOG'] : $symbol;
            $data = $this->getCurrentData($symbol);
            $result = [];

            for ($c = 0; $c < count($data); $c++) { 
                $result[$data[$c]->Symbol] = $data[$c]->LastTradePriceOnly;
            }

            return $result;
        }else
            return $this->getCurrentData($symbol)->LastTradePriceOnly;
    }

}

//Save Daily Price Info to CSV
     function Data2CSV_day($symbol,$name){
        $is_array = $symbol;
        $day_split = explode('volume', $is_array);
        //print_r($day_split);
        print_r('<br>');print_r('<br>');print_r('<br>');print_r('<br>');
        $day_split2 = $day_split[2];
        $Data = preg_split('/\s+/', $day_split2);
        $num = count($Data); 
        //print_r($num); print_r("\t");
        //print_r($Data[$num-3]);print_r("\t");
        //creat empty csv to store real-time data
        $filename = $name.".csv";
        $stock_name = preg_split('/[+\s_-]/', $name);;
       $file = fopen($filename,'w');

        $file2 = fopen($stock_name[0].".csv",'w');
        $Data_sub2 = preg_split('/[\s,]+/',$Data[$num-3]);
        $Data_sub2[0] = UNIX_Cov($Data_sub2[0]);
        $Data_sub3[0] = $stock_name[0];
        $Data_sub3[1] = ' ';
        $Data_sub3[2]= $Data_sub2[0];
        $Data_sub3[3]= $Data_sub2[1];
        $Data_sub3[4]= $Data_sub2[2];
        $Data_sub3[5]= $Data_sub2[3];
        $Data_sub3[6]= $Data_sub2[4];
        $Data_sub3[7]= $Data_sub2[5];


       fputcsv($file2,$Data_sub3);
       fclose($file2);

        for($q = 1 ; $q < $num - 1 ; $q++){
                {       
                             $Data_sub = preg_split('/[\s,]+/',$Data[$q]);
                            $Data_sub[0] = UNIX_Cov($Data_sub[0]);
                            //iris add Stock Symbol
                            $Data_sub2[0] = $stock_name[0];
                            $Data_sub2[1] = ' ';
                            $Data_sub2[2]= $Data_sub[0];
                            $Data_sub2[3]= $Data_sub[1];
                            $Data_sub2[4]= $Data_sub[2];
                            $Data_sub2[5]= $Data_sub[3];
                            $Data_sub2[6]= $Data_sub[4];
                            $Data_sub2[7]= $Data_sub[5];
                             //print_r($Data_sub[$p]);print_r('<br>');
                                            }fputcsv($file,$Data_sub2);
             }
             fclose($file);
        }
        //Save Past Year Price Info to CSV
     function Data2CSV_Year($symbol,$name){
        $is_array = $symbol;
        $day_split = explode('volume', $is_array);
        //print_r($day_split);
        print_r('<br>');print_r('<br>');print_r('<br>');print_r('<br>');
        $day_split2 = $day_split[2];
        $Data = preg_split('/\s+/', $day_split2);
        $stock_name = preg_split('/[+\s_-]/', $name);;
        $num = count($Data);

        //creat empty csv to store real-time data
        $filename = $name.".csv";

        $file = fopen($filename,'w');

        for($q = 1 ; $q < $num - 1 ; $q++){
                 {       
                             $Data_sub = preg_split('/[\s,]+/',$Data[$q]);
                            $Data_sub2[0] = $stock_name[0]; 
                            $Data_sub2[1]= $Data_sub[0];
                            $Data_sub2[2] = ' ';
                            $Data_sub2[3]= $Data_sub[1];
                            $Data_sub2[4]= $Data_sub[2];
                            $Data_sub2[5]= $Data_sub[3];
                            $Data_sub2[6]= $Data_sub[4];
                            $Data_sub2[7]= $Data_sub[5];
                                            }
                                            fputcsv($file,$Data_sub2);                                            
             }
             fclose($file);
           
        }
//iris add function for js year's stock price gnerateio

        function Data2js($symbol,$name){
            $is_array = $symbol;
        $day_split = explode('volume', $is_array);
        //print_r($day_split);
        print_r('<br>');print_r('<br>');print_r('<br>');print_r('<br>');
        $day_split2 = $day_split[2];
        $Data = preg_split('/\s+/', $day_split2);
        $stock_name = preg_split('/[+\s_-]/', $name);;
        $num = count($Data);
        //creat empty csv to store real-time data
        $filename = $name.".js";

        $file = fopen($filename,'w');
        $file_head = ']';
        // fputcsv($file,$file_head);
        // fclose($file);
        $Data_avg = preg_split('/[\s,]+/',$Data[1]);
        for($q = 1 ; $q < $num - 1 ; $q++){
                 {       
                             $Data_sub = preg_split('/[\s,]+/',$Data[$q]);
                             if($Data_sub2) { fputcsv($file,$Data_sub2); }
                             else {$Data_sub2[0]= "["; 
                                    $Data_sub2[0] = 'data='.$Data_sub2[0];
                                   // $Data_sub2[0] = 'var'.$Data_sub2[0];
                                    fputcsv($file,$Data_sub2);}
                            
                            $Data_sub2[0]= '['.$q;
                            // $Data_sub2[2] = ' ';
                            $Data_sub2[1]= $Data_sub[4].']';
                            if($q == $num - 3 ) {$Data_sub2[2]= ']';}
                            else{ $Data_sub2[2]= '';}

                                            }                                                     
             }
             fputcsv($file, $file_head);
             fclose($file);

        }

// Function for  UNIX Timestamp conversion
        function UNIX_Cov($symbol){
            return $time = date("H:i:s", $symbol);
        }

        function joinFiles(array $files, $result) {
    if(!is_array($files)) {
        throw new Exception('`$files` must be an array');
    }

    $wH = fopen($result, "w+");

    foreach($files as $file) {
        $fh = fopen($file, "r");
        while(!feof($fh)) {
            fwrite($wH, fgets($fh));
        }
        echo('echo joinfiles');
        fclose($fh);
        unset($fh);

        fwrite($wH); //usually last line doesn't have a newline
    }
    fclose($wH);
    unset($wH);
}

$yahoo = new U_Yahoo();
date_default_timezone_set('EST');

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
//PART: I, Real-time stock information

print_r('REAL-TIME STOCK PRICE');print_r('<br>');
$RT_stock;
echo "<pre>";
echo date("Y-m-d ");print_r("\t");
echo date("G:i:s");print_r("\t");
print_r('GOOG');print_r("\t");
$google_temp = $yahoo->getCurrentQuote(['GOOG']);
print_r( $google_temp ['GOOG']);print_r("\t");

echo "</pre>";

echo "<pre>";
echo date("Y-m-d ");print_r("\t");
echo date("G:i:s");print_r("\t");
print_r('YHOO');print_r("\t");
$yahoo_temp = $yahoo->getCurrentQuote(['YHOO']);
print_r($yahoo_temp  ['YHOO']);print_r("\t");
echo "</pre>";

echo "<pre>";
echo date("Y-m-d ");print_r("\t");
echo date("G:i:s");print_r("\t");
print_r('BAC');print_r("\t");
$bac_temp = $yahoo->getCurrentQuote(['BAC']);
print_r(  $bac_temp ['BAC']);print_r("\t");
echo "</pre>";

echo "<pre>";
echo date("Y-m-d ");print_r("\t");
echo date("G:i:s");print_r("\t");
print_r('SINA');print_r("\t");
$sina_temp = $yahoo->getCurrentQuote(['SINA']);
print_r($sina_temp  ['SINA']);print_r("\t");
echo "</pre>";

echo "<pre>";
echo date("Y-m-d ");print_r("\t");
echo date("G:i:s");print_r("\t");
print_r('BABA');print_r("\t");
$baba_temp = $yahoo->getCurrentQuote(['BABA']);
print_r( $baba_temp ['BABA']);print_r("\t");
echo "</pre>";

// $file = fopen('Real-time-Price.txt','w');
// $RT_price = $baba_temp['BABA'].",".$google_temp['GOOG'].",".$bac_temp['BAC'].",".$yahoo_temp['YHOO'].",".$sina_temp['SINA'];
// fwrite($file, $RT_price);
// fclose($file);


//////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////
//PART: II, Real-time stock information in a day, time difference is one minute
copy('output/Title.csv','Title.csv');
echo "<pre>";
print_r('<br>');
print_r('<br>');
echo "</pre>";  
$GOOG_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/GOOG/chartdata;type=quote;range=1d/csv');
$YHOO_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/YHOO/chartdata;type=quote;range=1d/csv');
$BABA_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BABA/chartdata;type=quote;range=1d/csv');
$SINA_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/SINA/chartdata;type=quote;range=1d/csv');
$BAC_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BAC/chartdata;type=quote;range=1d/csv');
$TSLA_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/TSLA/chartdata;type=quote;range=1d/csv');
$TCEHY_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/TCEHY/chartdata;type=quote;range=1d/csv');
$COP_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/COP/chartdata;type=quote;range=1d/csv');
$NTES_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/NTES/chartdata;type=quote;range=1d/csv');
$WUBA_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/WUBA/chartdata;type=quote;range=1d/csv');
$MAR_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/MAR/chartdata;type=quote;range=1d/csv');
$JPM_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/JPM/chartdata;type=quote;range=1d/csv');
$NVDA_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/NVDA/chartdata;type=quote;range=1d/csv');
$BIDU_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BIDU/chartdata;type=quote;range=1d/csv');
$WB_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/WB/chartdata;type=quote;range=1d/csv');
$ADBE_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/ADBE/chartdata;type=quote;range=1d/csv');
$PSTG_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/PSTG/chartdata;type=quote;range=1d/csv');
$PANW_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/PANW/chartdata;type=quote;range=1d/csv');
$BLK_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BLK/chartdata;type=quote;range=1d/csv');
$NOC_day = file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/NOC/chartdata;type=quote;range=1d/csv');

// print_r(count($x3));
Data2CSV_day($GOOG_day ,"GOOG_day");
Data2CSV_day($YHOO_day ,"YHOO_day");
Data2CSV_day($BABA_day ,"BABA_day");
Data2CSV_day($SINA_day ,"SINA_day");
Data2CSV_day($BAC_day ,"BAC_day");
Data2CSV_day($TSLA_day ,"TSLA_day");
Data2CSV_day($TCEHY_day ,"TCEHY_day");
Data2CSV_day($COP_day ,"COP_day");
Data2CSV_day($NTES_day ,"NTES_day");
Data2CSV_day($WUBA_day ,"WUBA_day");
Data2CSV_day($MAR_day ,"MAR_day");
Data2CSV_day($JPM_day ,"JPM_day");
Data2CSV_day($NVDA_day ,"NVDA_day");
Data2CSV_day($BIDU_day ,"BIDU_day");
Data2CSV_day($WB_day ,"WB_day");
Data2CSV_day($ADBE_day ,"ADBE_day");
Data2CSV_day($PSTG_day ,"PSTG_day");
Data2CSV_day($PANW_day ,"PANW_day");
Data2CSV_day($BLK_day ,"BLK_day");
Data2CSV_day($NOC_day ,"NOC_day");



//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////




///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
//PART: III, Past year stock information, attributes including, time, open, high, low, close, volume

print_r('<br>');print_r('<br>');print_r('<br>');
$GOOG_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/GOOG/chartdata;type=quote;range=1y/csv');
$YHOO_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/YHOO/chartdata;type=quote;range=1y/csv');
$BABA_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BABA/chartdata;type=quote;range=1y/csv');
$SINA_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/SINA/chartdata;type=quote;range=1y/csv');
$BAC_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BAC/chartdata;type=quote;range=1y/csv');
$TSLA_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/TSLA/chartdata;type=quote;range=1y/csv');
$TCEHY_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/TCEHY/chartdata;type=quote;range=1y/csv');
$COP_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/COP/chartdata;type=quote;range=1y/csv');
$NTES_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/NTES/chartdata;type=quote;range=1y/csv');
$WUBA_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/WUBA/chartdata;type=quote;range=1y/csv');
$MAR_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/MAR/chartdata;type=quote;range=1y/csv');
$JPM_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/JPM/chartdata;type=quote;range=1y/csv');
$NVDA_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/NVDA/chartdata;type=quote;range=1y/csv');
$BIDU_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BIDU/chartdata;type=quote;range=1y/csv');
$WB_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/WB/chartdata;type=quote;range=1y/csv');
$ADBE_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/ADBE/chartdata;type=quote;range=1y/csv');
$PSTG_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/PSTG/chartdata;type=quote;range=1y/csv');
$PANW_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/PANW/chartdata;type=quote;range=1y/csv');
$BLK_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/BLK/chartdata;type=quote;range=1y/csv');
$NOC_year =file_get_contents('https://chartapi.finance.yahoo.com/instrument/1.0/NOC/chartdata;type=quote;range=1y/csv');

Data2CSV_year($GOOG_year,"GOOG_year");
Data2CSV_year($YHOO_year,"YHOO_year");
Data2CSV_year($BABA_year,"BABA_year");
Data2CSV_year($SINA_year,"SINA_year");
Data2CSV_year($BAC_year,"BAC_year");
Data2CSV_year($TSLA_year,"TSLA_year");
Data2CSV_year($TCEHY_year,"TCEHY_year");
Data2CSV_year($COP_year,"COP_year");
Data2CSV_year($NTES_year,"NTES_year");
Data2CSV_year($WUBA_year,"WUBA_year");
Data2CSV_year($MAR_year,"MAR_year");
Data2CSV_year($JPM_year,"JPM_year");
Data2CSV_year($NVDA_year,"NVDA_year");
Data2CSV_year($BIDU_year,"BIDU_year");
Data2CSV_year($WB_year,"WB_year");
Data2CSV_year($ADBE_year,"ADBE_year");
Data2CSV_year($PSTG_year,"PSTG_year");
Data2CSV_year($PANW_year,"PANW_year");
Data2CSV_year($BLK_year,"BLK_year");
Data2CSV_year($NOC_year,"NOC_year");

//iris test stock data to js format

Data2js($GOOG_year,'GOOG_year_js');
Data2js($YHOO_year,'YHOO_year_js');
Data2js($BABA_year,'BABA_year_js');
Data2js($SINA_year,'SINA_year_js');
Data2js($BAC_year,'BAC_year_js');
Data2js($TSLA_year,'TSLA_year_js');
Data2js($TCEHY_year,'TCEHY_year_js');
Data2js($COP_year,'COP_year_js');
Data2js($NTES_year,'NTES_year_js');
Data2js($WUBA_year,'WUBA_year_js');
Data2js($MAR_year,"MAR_year_js");
Data2js($JPM_year,"JPM_year_js");
Data2js($NVDA_year,"NVDA_year_js");
Data2js($BIDU_year,"BIDU_year_js");
Data2js($WB_year,"WB_year_js");
Data2js($ADBE_year,"ADBE_year_js");
Data2js($PSTG_year,"PSTG_year_js");
Data2js($PANW_year,"PANW_year_js");
Data2js($BLK_year,"BLK_year_js");
Data2js($NOC_year,"NOC_year_js");


Data2js($GOOG_day,'GOOG_day_js');
Data2js($YHOO_day,'YHOO_day_js');
Data2js($BABA_day,'BABA_day_js');
Data2js($SINA_day,'SINA_day_js');
Data2js($BAC_day,'BAC_day_js');
Data2js($TSLA_day,'TSLA_day_js');
Data2js($TCEHY_day,'TCEHY_day_js');
Data2js($COP_day,'COP_day_js');
Data2js($NTES_day,'NTES_day_js');
Data2js($WUBA_day,'WUBA_day_js');
Data2js($MAR_day ,"MAR_day_js");
Data2js($JPM_day ,"JPM_day_js");
Data2js($NVDA_day ,"NVDA_day_js");
Data2js($BIDU_day ,"BIDU_day_js");
Data2js($WB_day ,"WB_day_js");
Data2js($ADBE_day ,"ADBE_day_js");
Data2js($PSTG_day ,"PSTG_day_js");
Data2js($PANW_day ,"PANW_day_js");
Data2js($BLK_day ,"BLK_day_js");
Data2js($NOC_day ,"NOC_day_js");

//print_r($Google_year);
//////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////

//iris add code the php, save real-time csv data to the mysql database
//3/9/3017

// joinFiles(array('Title.csv',"GOOG.csv" ,"YHOO.csv" ,"BABA.csv" ,"SINA.csv" ,"BAC.csv" ,"TSLA.csv" ,"TCEHY.csv" ,"COP.csv" ,"NTES.csv" ,"WUBA.csv" ,"MAR.csv" ,"JPM.csv" ,"NVDA.csv" ,"BIDU.csv" ,"WB.csv" ,"ADBE.csv" ,"PSTG.csv" ,"PANW.csv" ,"BLK.csv" ,"NOC.csv"), 'PresentData.csv');

// joinFiles(array('Title.csv','GOOG_day.csv', 'GOOG_year.csv', 'YHOO_day.csv', 'YHOO_year.csv', 'BABA_day.csv', 'BABA_year.csv', 'SINA_day.csv', 'SINA_year.csv', 'BAC_day.csv', 'BAC_year.csv','TSLA_day.csv', 'TSLA_year.csv', 'TCEHY_day.csv', 'TCEHY_year.csv', 'COP_day.csv', 'COP_year.csv', 'NTES_day.csv', 'NTES_year.csv', 'WUBA_day.csv', 'WUBA_year.csv','MAR_day.csv', 'MAR_year.csv', 'JPM_day.csv', 'JPM_year.csv', 'NVDA_day.csv', 'NVDA_year.csv', 'BIDU_day.csv', 'BIDU_year.csv', 'WB_day.csv', 'WB_year.csv' ,'ADBE_day.csv', 'ADBE_year.csv', 'PSTG_day.csv', 'PSTG_year.csv', 'PANW_day.csv', 'PANW_year.csv', 'BLK_day.csv', 'BLK_year.csv', 'NOC_day.csv', 'NOC_year.csv' ), 'HistoricalData.csv');

joinFiles(array('Title.csv',"GOOG.csv" ,"YHOO.csv" ,"BABA.csv" ,"SINA.csv" ,"BAC.csv" ,"TSLA.csv" ,"TCEHY.csv" ,"COP.csv" ,"NTES.csv" ,"WUBA.csv" ), 'PresentData.csv');

joinFiles(array('Title.csv','GOOG_day.csv', 'GOOG_year.csv', 'YHOO_day.csv', 'YHOO_year.csv', 'BABA_day.csv', 'BABA_year.csv', 'SINA_day.csv', 'SINA_year.csv', 'BAC_day.csv', 'BAC_year.csv','TSLA_day.csv', 'TSLA_year.csv', 'TCEHY_day.csv', 'TCEHY_year.csv', 'COP_day.csv', 'COP_year.csv', 'NTES_day.csv', 'NTES_year.csv', 'WUBA_day.csv', 'WUBA_year.csv'), 'HistoricalData.csv');


copy('PresentData.csv','output/PresentData.csv');
copy('HistoricalData.csv','output/HistoricalData.csv');

//generate js files base on the year's stock data
//copy('BABA_year_js.txt','BABA_year_js.js');

//clean the csv files int eh whole folder
$files = glob('*.csv'); // get all file names
foreach($files as $file){ // iterate files
  if(is_file($file))
    unlink($file); // delete file
}

//clean the txt files int eh whole folder
$files = glob('*.txt'); // get all file names
foreach($files as $file){ // iterate files
  if(is_file($file))
    unlink($file); // delete file
}

//end of import data to mysql database
