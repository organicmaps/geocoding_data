#!/usr/bin/env python3
import sys
import json
import csv
import re
from collections import defaultdict

COUNTRIES = [
    ('Afghanistan', 'AF', 'Kabul'),
    ('Albania', 'AL', 'Tirana'),
    ('Algeria', 'DZ', 'Algiers'),
    ('Andorra', 'AD', 'Andorra La Vella'),
    ('Angola', 'AO', 'Luanda'),
    ('Anguilla', 'AI', 'The Valley'),
    ('Antigua and Barbuda', 'AG', 'St. John\'s'),
    ('Argentina', 'AR', 'Buenos Aires'),
    ('Armenia', 'AM', 'Yerevan'),
    ('Australia', 'AU', 'Canberra'),
    ('Austria', 'AT', 'Vienna'),
    ('Azerbaijan', 'AZ', 'Baku'),
    ('Bahrain', 'BH', 'Manama'),
    ('Bangladesh', 'BD', 'Dhaka'),
    ('Barbados', 'BB', 'Bridgetown'),
    ('Belarus', 'BY', 'Minsk'),
    ('Belgium', 'BE', 'Brussels'),
    ('Belize', 'BZ', 'Belmopan'),
    ('Benin', 'BJ', 'Porto-Novo'),
    ('Bermuda', 'BM', 'Hamilton'),
    ('Bhutan', 'BT', 'Thimphu'),
    ('Bolivia', 'BO', 'Sucre'),
    ('Bosnia and Herzegovina', 'BA', 'Sarajevo'),
    ('Botswana', 'BW', 'Gaborone'),
    ('Brazil', 'BR', 'Brasilia'),
    ('British Indian Ocean Territory', 'IO', 'Camp Justice'),
    ('British Virgin Islands', 'VG', 'Road Town'),
    ('Brunei', 'BN', 'Bandar Seri Begawan'),
    ('Bulgaria', 'BG', 'Sofia'),
    ('Burkina Faso', 'BF', 'Ouagadougou'),
    ('Burundi', 'BI', 'Bujumbura'),
    ('Cambodia', 'KH', 'Phnom Penh'),
    ('Cameroon', 'CM', 'Yaounde'),
    ('Canada', 'CA', 'Ottawa'),
    ('Cape Verde', 'CV', 'Praia'),
    ('Cayman Islands', 'KY', 'George Town'),
    ('Central African Republic', 'CF', 'Bangui'),
    ('Chad', 'TD', 'N\'Djamena'),
    ('Chile', 'CL', 'Santiago'),
    ('China', 'CN', 'Beijing'),
    ('Colombia', 'CO', 'Bogotá'),
    ('Comoros', 'KM', 'Moroni'),
    ('Congo-Brazzaville', 'CG', 'Brazzaville'),
    ('Cook Islands', 'CK', 'Avarua'),
    ('Costa Rica', 'CR', 'San José'),
    ('Croatia', 'HR', 'Zagreb'),
    ('Cuba', 'CU', 'Havana'),
    ('Cyprus', 'CY', 'Nicosia'),
    ('Czechia', 'CZ', 'Prague'),
    ('Côte d\'Ivoire', 'CI', 'Yamoussoukro'),
    ('Democratic Republic of the Congo', 'CD', 'Kinshasa'),
    ('Denmark', 'DK', 'Copenhagen'),
    ('Djibouti', 'DJ', 'Djibouti'),
    ('Dominica', 'DM', 'Roseau'),
    ('Dominican Republic', 'DO', 'Santo Domingo'),
    ('East Timor', 'TL', 'Dili'),
    ('Ecuador', 'EC', 'Quito'),
    ('Egypt', 'EG', 'Cairo'),
    ('El Salvador', 'SV', 'San Salvador'),
    ('Equatorial Guinea', 'GQ', 'Malabo'),
    ('Eritrea', 'ER', 'Asmara'),
    ('Estonia', 'EE', 'Tallinn'),
    ('eSwatini', 'SZ', 'Mbabane'),
    ('Ethiopia', 'ET', 'Addis Ababa'),
    ('Falkland Islands', 'FK', 'Stanley'),
    ('Faroe Islands', 'FO', 'Tórshavn'),
    ('Federated States of Micronesia', 'FM', 'Palikir'),
    ('Fiji', 'FJ', 'Suva'),
    ('Finland', 'FI', 'Helsinki'),
    ('France', 'FR', 'Paris'),
    ('Gabon', 'GA', 'Libreville'),
    ('Gambia', 'GM', 'Banjul'),
    ('Georgia', 'GE', 'Tbilisi'),
    ('Germany', 'DE', 'Berlin'),
    ('Ghana', 'GH', 'Accra'),
    ('Gibraltar', 'GI', 'Gibraltar'),
    ('Greece', 'GR', 'Athens'),
    ('Greenland', 'GL', 'Nuuk'),
    ('Grenada', 'GD', 'St. George\'s'),
    ('Guatemala', 'GT', 'Guatemala City'),
    ('Guernsey', 'GG', 'Saint Peter Port'),
    ('Guinea', 'GN', 'Conakry'),
    ('Guinea-Bissau', 'GW', 'Bissau'),
    ('Guyana', 'GY', 'Georgetown'),
    ('Haiti', 'HT', 'Port-Au-Prince'),
    ('Honduras', 'HN', 'Tegucigalpa'),
    ('Hungary', 'HU', 'Budapest'),
    ('Iceland', 'IS', 'Reykjavík'),
    ('India', 'IN', 'New Delhi'),
    ('Indonesia', 'ID', 'Jakarta'),
    ('Iran', 'IR', 'Tehran'),
    ('Iraq', 'IQ', 'Baghdad'),
    ('Ireland', 'IE', 'Dublin'),
    ('Isle of Man', 'IM', 'Douglas'),
    ('Israel', 'IL', 'Tel Aviv'),
    ('Italy', 'IT', 'Rome'),
    ('Jamaica', 'JM', 'Kingston'),
    ('Japan', 'JP', 'Tokyo'),
    ('Jersey', 'JE', 'Saint Helier'),
    ('Jordan', 'JO', 'Amman'),
    ('Kazakhstan', 'KZ', 'Astana'),
    ('Kenya', 'KE', 'Nairobi'),
    ('Kiribati', 'KI', 'South Tarawa'),
    ('Kosovo', 'XK', 'Pristina'),
    ('Kuwait', 'KW', 'Kuwait City'),
    ('Kyrgyzstan', 'KG', 'Bishkek'),
    ('Laos', 'LA', 'Vientiane'),
    ('Latvia', 'LV', 'Riga'),
    ('Lebanon', 'LB', 'Beirut'),
    ('Lesotho', 'LS', 'Maseru'),
    ('Liberia', 'LR', 'Monrovia'),
    ('Libya', 'LY', 'Tripoli'),
    ('Liechtenstein', 'LI', 'Vaduz'),
    ('Lithuania', 'LT', 'Vilnius'),
    ('Luxembourg', 'LU', 'Luxembourg'),
    ('Macedonia', 'MK', 'Skopje'),
    ('Madagascar', 'MG', 'Antananarivo'),
    ('Malawi', 'MW', 'Lilongwe'),
    ('Malaysia', 'MY', 'Kuala Lumpur'),
    ('Maldives', 'MV', 'Malé'),
    ('Mali', 'ML', 'Bamako'),
    ('Malta', 'MT', 'Valletta'),
    ('Marshall Islands', 'MH', 'Majuro'),
    ('Mauritania', 'MR', 'Nouakchott'),
    ('Mauritius', 'MU', 'Port Louis'),
    ('Mexico', 'MX', 'Mexico City'),
    ('Moldova', 'MD', 'Chișinău'),
    ('Monaco', 'MC', 'Monaco'),
    ('Mongolia', 'MN', 'Ulaanbaatar'),
    ('Montenegro', 'ME', 'Podgorica'),
    ('Montserrat', 'MS', 'Brades'),
    ('Morocco', 'MA', 'Rabat'),
    ('Mozambique', 'MZ', 'Maputo'),
    ('Myanmar', 'MM', 'Naypyidaw'),
    ('Namibia', 'NA', 'Windhoek'),
    ('Nauru', 'NR', 'Yaren'),
    ('Nepal', 'NP', 'Kathmandu'),
    ('New Zealand', 'NZ', 'Wellington'),
    ('Nicaragua', 'NI', 'Managua'),
    ('Niger', 'NE', 'Niamey'),
    ('Nigeria', 'NG', 'Abuja'),
    ('Niue', 'NU', 'Alofi'),
    ('North Korea', 'KP', 'Pyongyang'),
    ('Norway', 'NO', 'Oslo'),
    ('Oman', 'OM', 'Muscat'),
    ('Palau', 'PW', 'Ngerulmud'),
    ('Palestinian Territories', 'PS', 'Ramallah'),
    ('Pakistan', 'PK', 'Islamabad'),
    ('Panama', 'PA', 'Panama City'),
    ('Papua New Guinea', 'PG', 'Port Moresby'),
    ('Paraguay', 'PY', 'Asunción'),
    ('Peru', 'PE', 'Lima'),
    ('Philippines', 'PH', 'Manila'),
    ('Pitcairn Islands', 'PN', 'Adamstown'),
    ('Poland', 'PL', 'Warsaw'),
    ('Portugal', 'PT', 'Lisbon'),
    ('Qatar', 'QA', 'Doha'),
    ('Romania', 'RO', 'Bucharest'),
    ('Russia', 'RU', 'Moscow'),
    ('Rwanda', 'RW', 'Kigali'),
    ('Saint Helena, Ascension and Tristan da Cunha', 'SH', 'Jamestown'),
    ('Saint Kitts and Nevis', 'KN', 'Basseterre'),
    ('Saint Lucia', 'LC', 'Castries'),
    ('Saint Vincent and the Grenadines', 'VC', 'Kingstown'),
    ('Samoa', 'WS', 'Apia'),
    ('San Marino', 'SM', 'City Of San Marino'),
    ('Saudi Arabia', 'SA', 'Riyadh'),
    ('Senegal', 'SN', 'Dakar'),
    ('Serbia', 'RS', 'Belgrade'),
    ('Seychelles', 'SC', 'Victoria'),
    ('Sierra Leone', 'SL', 'Freetown'),
    ('Singapore', 'SG', 'Singapore'),
    ('Slovakia', 'SK', 'Bratislava'),
    ('Slovenia', 'SI', 'Ljubljana'),
    ('Solomon Islands', 'SB', 'Honiara'),
    ('Somalia', 'SO', 'Mogadishu'),
    ('South Africa', 'ZA', 'Pretoria'),
    ('South Georgia and the South Sandwich Islands', 'GS', 'King Edward Point'),
    ('South Korea', 'KR', 'Seoul'),
    ('South Sudan', 'SS', 'Juba'),
    ('Spain', 'ES', 'Madrid'),
    ('Sri Lanka', 'LK', 'Sri Jayawardenepura Kotte'),
    ('Sudan', 'SD', 'Khartoum'),
    ('Suriname', 'SR', 'Paramaribo'),
    ('Sweden', 'SE', 'Stockholm'),
    ('Switzerland', 'CH', 'Bern'),
    ('Syria', 'SY', 'Damascus'),
    ('São Tomé and Príncipe', 'ST', 'São Tomé'),
    ('Taiwan', 'TW', 'Taipei'),
    ('Tajikistan', 'TJ', 'Dushanbe'),
    ('Tanzania', 'TZ', 'Dodoma'),
    ('Thailand', 'TH', 'Bangkok'),
    ('The Bahamas', 'BS', 'Nassau'),
    ('The Netherlands', 'NL', 'Amsterdam'),
    ('Togo', 'TG', 'Lomé'),
    ('Tokelau', 'TK', 'Fakaofo'),
    ('Tonga', 'TO', 'Nuku\'alofa'),
    ('Trinidad and Tobago', 'TT', 'Port Of Spain'),
    ('Tunisia', 'TN', 'Tunis'),
    ('Turkey', 'TR', 'Ankara'),
    ('Turkmenistan', 'TM', 'Ashgabat'),
    ('Turks and Caicos Islands', 'TC', 'Cockburn Town'),
    ('Tuvalu', 'TV', 'Vaiaku'),
    ('Uganda', 'UG', 'Kampala'),
    ('Ukraine', 'UA', 'Kyiv'),
    ('United Arab Emirates', 'AE', 'Abu Dhabi'),
    ('United Kingdom', 'GB', 'London'),
    ('United States of America', 'US', 'Washington, D.C.'),
    ('Uruguay', 'UY', 'Montevideo'),
    ('Uzbekistan', 'UZ', 'Tashkent'),
    ('Vanuatu', 'VU', 'Port Vila'),
    ('Vatican City', 'VA', 'Vatican City'),
    ('Venezuela', 'VE', 'Caracas'),
    ('Vietnam', 'VN', 'Hanoi'),
    ('Yemen', 'YE', 'Sana\'a'),
    ('Zambia', 'ZM', 'Lusaka'),
    ('Zimbabwe', 'ZW', 'Harare'),
]

CITY_NAMES = ['Tokyo', 'Aba', 'Abeokuta', 'Abia', 'Abidjan', 'Abobo',
              'Abu Dhabi', 'Abu Ghraib', 'Acapulco', 'Accra', 'Dammam',
              'Ad Diwaniyah', 'Adalia', 'Adana', 'Addis Ababa', 'Adelaide',
              'Aden', 'Adiyaman', 'Agadir', 'Agra', 'Aguascalientes',
              'Ahmadabad', 'Ahvaz', 'Aydin', 'Ajmer', 'Akola', 'Basra',
              'Al Basrah Al Qadimah', 'El Jadida', 'Kuwait City',
              'Mosul', 'Al Qahirah', 'Sharjah',
              'Albuquerque', 'Aleksandrovsk', 'Aleppo', 'Alexandria',
              'Algiers', 'Aligarh', 'Allahabad', 'Almaty', 'Amagasaki',
              'Amaravati', 'Amman', 'Amravati', 'Amritsar', 'Amsterdam',
              'Najaf', 'Ananindeua', 'Ankara', 'Ansan', 'Anshan', 'Antalya',
              'Antananarivo', 'Antipolo', 'Antwerp', 'Anyang', 'Anyang',
              'Aracaju', 'Arak', 'Arequipa', 'As Sulaymaniyah', 'Suez',
              'Asansol', 'Ashgabat', 'Ash Shariqah', 'Ashgabat', 'Asmara',
              'Astrakhan', 'Astrida', 'Asuncion', 'Athens', 'Aurangabad',
              'Austin', 'Azadshahr', 'Azilal', 'Bacolod', 'Bacolod City',
              'Baghdad', 'Bahawalpur', 'Baku',
              'Balikpapan', 'Baltimore', 'Bamako', 'Bandar Lampung', 'Bandung',
              'Bengaluru', 'Bangkok', 'Bangui', 'Banjarmasin', 'Baoding',
              'Baoji', 'Baotou', 'Barcelona', 'Bareli', 'Barnaul',
              'Barquisimeto', 'Barranquilla', 'Beijing', 'Beira', 'Beirut',
              'Phetchaburi', 'Bekasi', 'Belem', 'Belfast', 'Belford Roxo',
              'Belgaum', 'Belgrade', 'Belo Horizonte', 'Bengbu', 'Benghazi',
              'Benin City', 'Benoni', 'Benxi', 'Berlin', 'Bhatpara', 'Bhavnagar',
              'Bhilai', 'Bhiwandi', 'Bhopal', 'Bhubaneswar', 'Bikaner',
              'Birmingham', 'Bishkek', 'Blantyre', 'Bloemfontein',
              'Bogor', 'Bogota', 'Boksburg', 'Bombay', 'Port Said',
              'Sarajevo', 'Bouake', 'Brampton', 'Brasilia', 'Brazzaville',
              'Bremen', 'Brisbane', 'Bristol', 'Brooklyn', 'Bursa',
              'Brussels', 'Bucaramanga', 'Bucharest', 'Budapest',
              'Buenos Aires', 'Bulawayo', 'Bursa', 'Busan',
              'Caesarea', 'Cagayan De Oro', 'Calabar', 'Calcutta', 'Calgary',
              'Cali', 'Kozhikode', 'Callao', 'Campinas',
              'Campo Grande', 'Cancun', 'Cangzhou', 'Cape Town', 'Caracas',
              'Carrefour', 'Cartagena', 'Casablanca', 'Cebu City',
              'Central', 'Chanthaburi', 'Chandigarh', 'Changchun', 'Changde',
              'Changsha', 'Changzhou', 'Charlotte', 'Cheboksary',
              'Chelyabinsk', 'Cheng', 'Chengde', 'Chengdu', 'Chiba', 'Chicago',
              'Chiclayo', 'Chihuahua', 'Cimahi', 'Chimalhuacan', 'Chișinău',
              'Chittagong', 'Chitungwiza', 'Chkalov', 'Chongqing', 'Jeonju',
              'Cibitoke', 'Ciudad Guayana',
              'Ciudad Juarez', 'Cleveland', 'Cluj-Napoca', 'Cochabamba', 'Coimbatore',
              'Cologne', 'Colombo', 'Columbus', 'Constantine',
              'Contagem', 'Copenhagen', 'Cordoba', 'Cotonou',
              'Cuautitlan Izcalli', 'Cucuta', 'Cuiaba', 'Culiacan', 'Curitiba',
              'Cuttack', 'Danang', 'Daejeon',
              'Dagon', 'Dagu', 'Dakar', 'Dalian', 'Dallas', 'Damascus',
              'Dandong', 'Dang', 'Dar Es Salaam', 'Dasmarinas', 'Dasmarinas',
              'Datong', 'Davao', 'Davao City', 'Dehradun', 'Delhi', 'Denver',
              'Depok', 'Detroit', 'Dhaka', 'Diyarbakir',
              'Dushanbe', 'Dongliao', 'Dortmund', 'Douala', 'Dresden',
              'Dubai', 'Dublin', 'Duisburg', 'Duque De Caxias',
              'Durango', 'Durban', 'Durgapur', 'Dusseldorf', 'Ecatepec de Morelos',
              'Edessa', 'Edinburgh', 'Edmonton', 'Edo', 'Elko',
              'El Mahalla El Kubra', 'El Paso', 'Al Hudaydah', 'Elazig',
              'Enugu', 'Erzurum', 'Isfahan', 'Eskisehir', 'Essaouira', 'Essen',
              'Faisalabad', 'Faridabad', 'Feira De Santana',
              'Fez', 'Kousseri', 'Fort Worth', 'Foshan',
              'Frankfurt Am Main', 'Freetown', 'Fresno', 'Fukuoka', 'Funabashi',
              'Fushun', 'Fuxin', 'Fuzhou', 'Tabuk', 'Kamphaeng Phet', 'Garoua',
              'Gaziantep', 'Gdansk', 'General Santos', 'Geneve', 'Genova',
              'Ghaziabad', 'Qom', 'Giza', 'Glasgow', 'Goiania', 'Gold Coast',
              'Homel', 'Gorakhpur', 'Gothenburg', 'Guadalajara',
              'Guadalupe', 'Guangzhou', 'Guarulhos', 'Guatemala', 'Guayaquil',
              'Guilin', 'Guiyang', 'Gujranwala', 'Kalaburagi', 'Guntur',
              'Guwahati', 'Gwalior', 'Hanoi', 'Hachioji', 'Haiphong',
              'Haikou', 'Hamadan', 'Hamah', 'Hamamatsu', 'Hamburg', 'Hamhung',
              'Hamilton', 'Hamitabat', 'Handan', 'Hangzhou', 'Hanover', 'Howrah',
              'Harare', 'Harbin', 'Hargeisa', 'Havana', 'Hefei', 'Hegang',
              'Helsinki', 'Hengshui', 'Hengyang', 'Hermosillo', 'Himeji',
              'Homs', 'Hiroshima', 'Ho Chi Minh City', 'Hohhot', 'Hong Kong',
              'Houston', 'Huaibei', 'Huainan', 'Huai\'an', 'Hubballi', 'Hyderabad',
              'Hyderabad', 'Ibadan', 'Ichikawa', 'Ilorin', 'Indianapolis',
              'Indore', 'Ipoh', 'Iquitos', 'Erbil', 'Irkutsk', 'Islamabad',
              'Istanbul', 'Izhevsk', 'Izmir', 'Jabalpur', 'Jaboatao dos Guararapes',
              'Jacksonville', 'Jaipur', 'Jizan', 'Jakarta', 'Jalandhar',
              'Jammu', 'Jamnagar', 'Jamshedpur', 'Jerusalem',
              'Jiamusi', 'Jiangmen', 'Jiaojiang', 'Jiaozuo', 'Jiaxing',
              'Djibouti', 'Jeddah', 'Jilin', 'Jinan', 'Jining', 'Joao Pessoa',
              'Jodhpur', 'Johannesburg', 'Johor Bahru', 'Joinville', 'Jos',
              'Juarez', 'Juiz De Fora', 'Kabul', 'Kaduna', 'Kagoshima',
              'Kahriz', 'Kaifeng', 'Kalat',
              'Kaliningrad', 'Kalyan', 'Kampala', 'Kananga', 'Kanazawa', 'Kano',
              'Kanpur', 'Kansas City', 'Kaohsiung', 'Karachi',
              'Karaj', 'Kathmandu', 'Katsina', 'Kawaguchi', 'Kawasaki',
              'Kawasaki', 'Kayseri', 'Kazan', 'Kemerovo', 'Kerman',
              'Kermanshah', 'Khabarovsk', 'Kharkiv', 'Khartoum', 'Khemisset',
              'Khenifra', 'Khouribga', 'Khulna', 'Kyiv', 'Kigali',
              'Kingston', 'Kinshasa', 'Kirkuk', 'Kirov', 'Kisangani',
              'Kitakyushu', 'Klang', 'Kobe', 'Kocaeli', 'Kochi',
              'Kolhapur', 'Konia', 'Konya', 'Kosovo', 'Kota', 'Kota Kinabalu',
              'Kousseri', 'Krakow', 'Krasnodar', 'Krasnoyarsk',
              'Kryvyi Rih', 'Kuala Lumpur', 'Kuching', 'Kumamoto', 'Kumasi',
              'Kunming', 'Kurashiki', 'Gwangju', 'Kyoto', 'La Paz', 'La Plata',
              'Lagos', 'Lahore', 'Lucknow', 'Langfang', 'Lanzhou', 'Larache',
              'Las Pinas', 'Las Vegas', 'Leeds', 'Leipzig', 'Leon', 'Lehi',
              'Liaoyang', 'Libreville', 'Lilongwe', 'Lima', 'Lipetsk', 'Lisboa',
              'Liuzhou', 'Liverpool', 'Lopburi', 'Lodz', 'Lome', 'London',
              'Londrina', 'Long Beach', 'López Mateos City', 'Los Angeles',
              'Luancheng', 'Luanda', 'Lubumbashi', 'Ludhiana', 'Luoyang',
              'Lusaka', 'Lviv', 'Lyon', 'Ma\'anshan', 'Maceio', 'Madras',
              'Madrid', 'Madurai', 'Maha Sarakham', 'Maiduguri', 'Mysuru',
              'Makasar', 'Makhachkala', 'Malaga', 'Malang', 'Malatya',
              'Malatya', 'Malegaon', 'Manado', 'Managua', 'Manaus', 'Mandalay',
              'Manila', 'Mansilingan', 'Maoming', 'Maputo', 'Mar Del Plata',
              'Maracaibo', 'Marrakesh', 'Marseille', 'Mashhad', 'Matamoros',
              'Matola', 'Matsudo', 'Matsuyama', 'Mawlamyine', 'Mbuji-mayi',
              'Mecca', 'Medan', 'Medellin', 'Medina', 'Meerut', 'Meknes',
              'Melbourne', 'Memphis', 'Mendoza', 'Merida', 'Mersin', 'Mesa',
              'Mexicali', 'Mexico', 'Milan', 'Milwaukee', 'Minsk',
              'Mississauga', 'Mixco', 'Mogadishu', 'Mombasa', 'Monrovia',
              'Monterrey', 'Montevideo', 'Montreal', 'Moradabad', 'Morelia',
              'Moscow', 'Mosul', 'Mudanjiang', 'Multan', 'Munich', 'Mwanza',
              'Naberezhnye Chelny', 'Nakhon Pathom', 'Nagoya', 'Nagpur',
              'Nairobi', 'Namangan', 'Nanchang', 'Nanded', 'Nanjing',
              'Nanning', 'Nantong', 'Naples', 'Napoli', 'Narathiwat',
              'Nashville', 'Nashik', 'Natal', 'Naucalpan de Juarez', 'Neijiang', 'Nerima',
              'New Orleans', 'New York',
              'Newcastle', 'Nezahualcoyotl', 'Niamey', 'Niigata', 'Mykolaiv',
              'Ningbo', 'Nishinomiya', 'Niteroi', 'Nizhny Novgorod',
              'North Kansas City', 'Nouakchott', 'Novokuznetsk',
              'Novosibirsk', 'Nuremberg', 'Odessa', 'Ogun', 'Ooita', 'Okayama',
              'Okene', 'Oklahoma City', 'Omdurman', 'Omsk', 'Onicha', 'Onitsha',
              'Orenburg', 'Urmia', 'Osaka', 'Osasco', 'Osogbo', 'Oslo',
              'Ottawa', 'Ouagadougou', 'Ouagadougou', 'Ouarzazate', 'Oyo',
              'Padang', 'Pathum Thani', 'Palembang', 'Palermo',
              'Panshan', 'Panzhihua', 'Paris', 'Patna', 'Penza',
              'Pereira', 'Perm', 'Perth', 'Peshawar', 'Petaling Jaya',
              'Philadelphia', 'Phnom Penh', 'Phoenix', 'Pietermaritzburg',
              'Pimpri', 'Pingdingshan', 'Pointe-noire', 'Pontianak',
              'Port Elizabeth', 'Port Harcourt', 'Port-au-prince', 'Portland',
              'Porto Alegre', 'Poti', 'Poznan', 'Praha', 'Pretoria', 'Puebla',
              'Pune', 'Puyang', 'Pyongyang', 'Qingdao', 'Qinhuangdao',
              'Qiqihar', 'Qom', 'Quebec', 'Queretaro', 'Quetta', 'Quezon',
              'Quilmes', 'Quito', 'Rabat', 'Raipur', 'Rajkot', 'Rajpur',
              'Rajshahi', 'Ranchi', 'Rasht', 'Rawalpindi', 'Recife',
              'Reynosa', 'Ribeirao Preto', 'Riga', 'Rio De Janeiro', 'Riyadh',
              'Rome', 'Rongcheng', 'Rosario', 'Rostov-na-donu', 'Rotterdam',
              'Ryazan', 'Sacramento', 'Safi', 'Sagamihara',
              'Saharanpur', 'Saint Petersburg', 'Sakai', 'Sale', 'Salta',
              'Saltillo', 'Salvador', 'Samara', 'San Antonio', 'San Diego',
              'San Francisco', 'San Jose', 'San Juan', 'San Luis Potosi',
              'San Miguel De Tucuman', 'San Nicolas De Los Garza',
              'San Pedro Sula', 'San Salvador', 'Sana\'a',
              'Santa Cruz De La Sierra', 'Santa Fe', 'Santa Marta', 'Santiago',
              'Santiago', 'Santiago De Cuba', 'Santo Andre', 'Santo Domingo',
              'Sao Bernardo Do Campo', 'Sao Goncalo', 'Sao Joao De Meriti',
              'Sao Jose Dos Campos', 'Sao Luis', 'São Paulo', 'Sapporo',
              'Sar-e Pol', 'Saratov', 'Sargodha', 'Seattle',
              'Semarang', 'Sendai', 'Seoul', 'Settat', 'Sevilla', 'Shah Alam',
              'Shanghai', 'Shantou', 'Shaoguan', 'Sharjah', 'Shashi',
              'Sheffield', 'Shenyang', 'Shenzhen', 'Shihezi', 'Siliguri',
              'Shiraz', 'Shizuoka', 'Solapur', 'Sialkot', 'Singapore',
              'Skopje', 'Sofia', 'Sokoto', 'Songnam', 'Sorocaba',
              'South Boston', 'Soweto', 'Srinagar', 'Stockholm',
              'Stuttgart', 'Surabaya', 'Surakarta',
              'Surat', 'Suwon', 'Suzhou', 'Sydney', 'Tabriz', 'Daegu',
              'Taguig', 'Taian', 'Taichung', 'Tainan', 'Taipei', 'Taiyuan',
              'Taizhou', 'Tangier', 'Tangerang', 'Tanggu', 'Tangier',
              'Tangshan', 'Taounate', 'Taroudant', 'Tashkent', 'Taza',
              'Tbilisi', 'Tegucigalpa', 'Tehran', 'Tembisa', 'Teresina',
              'Thana', 'The Hague', 'Thiruvananthapuram', 'Tianjin', 'Tijuana',
              'Tipaza', 'Tiruchirappalli', 'Tirunelveli', 'Tlalnepantla',
              'San Pedro Tlaquepaque', 'Toluca', 'Tolyatti', 'Tomsk', 'Torino', 'Toronto',
              'Torreon', 'Tripoli', 'Trujillo', 'Tucson', 'Tucuman', 'Tula',
              'Tunes', 'Turin', 'Tuxtla Gutierrez', 'Tyumen', 'Uberlandia',
              'Ufa', 'Uijeongbu', 'Ujjain', 'Ulhasnagar', 'Ulyanovsk',
              'Urfa', 'Urumqi', 'Ussuriysk',
              'Utsunomiya', 'Vadodara', 'Valencia', 'Valencia', 'Vancouver',
              'Varanasi', 'Vaucluse', 'Veracruz', 'Vereeniging', 'Vijayawada',
              'Vilnius', 'Virginia Beach', 'Visakhapatnam', 'Vladivostok',
              'Volgograd', 'Voronezh', 'Oran', 'Warrap', 'Warangal',
              'Warri', 'Warsaw', 'Washington', 'Welkom', 'Wenzhou', 'Wien',
              'Winnipeg', 'Wroclaw', 'Wuhan', 'Wuhu', 'Wuxi', 'Xiamen', 'Xi\'an',
              'Xianyang', 'Xingtai', 'Xining', 'Xinxiang',
              'Xinyang', 'Xuchang', 'Xuzhou', 'Yancheng', 'Yangzhou', 'Yantai',
              'Yaounde', 'Yaroslavl', 'Yazd', 'Yekaterinburg', 'Yerevan',
              'Yichang', 'Yinchuan', 'Yingkou', 'Yogyakarta', 'Yokohama',
              'Yokosuka', 'Yongkang', 'Yueyang', 'Yunfu', 'Zagreb',
              'Zahedan', 'Zamboanga', 'Zamboanga City', 'Zapopan', 'Zaragoza',
              'Zaria', 'Zhangjiakou', 'Zhangzhou', 'Zhanjiang', 'Zhengzhou',
              'Zhenjiang', 'Zhuhai', 'Zhuzhou', 'Zibo', 'Zigong', 'Zunyi']


def read_csv_into_dict(f):
    r = csv.reader(f, delimiter=';')
    header = next(r)
    result = {}
    for row in r:
        item = {}
        for i in range(1, len(row)):
            item[header[i]] = row[i]
        result[row[0]] = item
    return result

if len(sys.argv) < 2:
    print('Usage: {} <path_to_places_json_or_csv>'.format(sys.argv[0]))
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    if '.csv' in sys.argv[1]:
        places = read_csv_into_dict(f)
    else:
        places = json.load(f)

countries_name = re.sub(r'places(?=[._-])', 'countries', sys.argv[1])
with open(countries_name, 'r') as f:
    if '.csv' in countries_name:
        countries = read_csv_into_dict(f)
    else:
        countries = json.load(f)

regions_name = re.sub(r'places(?=[._-])', 'regions', sys.argv[1])
with open(regions_name, 'r') as f:
    if '.csv' in regions_name:
        regions = read_csv_into_dict(f)
    else:
        regions = json.load(f)

country_iso = {}
for country in countries.values():
    name = None
    for k in ('name_en', 'int_name', 'name'):
        if k in country:
            name = country[k]
            break
    country_iso[name.lower()] = country['iso']

for region in regions.values():
    if region.get('iso'):
        if region['iso'][:2] != countries[str(region['country'])].get('iso'):
            print('Wrong ISO for a region {}: {} and country has {}'.format(
                region['name'], region['iso'], countries[str(region['country'])].get('iso')))

place_names = defaultdict(list)
for pid, names in places.items():
    for k in ('name_en', 'int_name', 'name'):
        if k in names:
            place_names[names[k].lower()].append(pid)

for city in CITY_NAMES:
    if city.lower() not in place_names:
        print('City not found: {}'.format(city))

for country, iso, city in COUNTRIES:
    osm_iso = country_iso.get(country.lower(), None)
    if osm_iso is None:
        print('Missing country: {}'.format(country))
    elif osm_iso != iso:
        print('Country {} got iso code {}, should have {}'.format(country, osm_iso, iso))

for country, iso, city in COUNTRIES:
    pids = place_names.get(city.lower())
    if not pids:
        print('Capital not found: {}, {}'.format(city, country))
    else:
        pcountries = set()
        for pid in pids:
            for k, name in countries.get(str(places[pid]['country']), {}).items():
                if k in ('name_en', 'int_name', 'name'):
                    pcountries.add(name.lower())
                    if name.lower() == country.lower():
                        print('Capital {},{}'.format(city, pid))
        if country.lower() not in pcountries:
            print('Country {} for capital {} not found, instead: {}'.format(
                country, city, ', '.join([c.title() for c in sorted(pcountries)])))
