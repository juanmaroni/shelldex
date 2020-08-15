from typing import List
import requests
import json
import random

missingno_ascii: str = '''
################@@##########   ## z ##  ## #############
########################### `` zz#  # ++  #@@###########
###########################    # #z  `   z*#############
##########################@   ` #+` # + z*##@#@#########
#########################@# ##*#    # # #  @@###########
########################@##:  .  +#z #`+ +z##@@@########
##########################@#;#,@:@:#  z++z @############
#########################@##;:;;:;:# z+##+ #@###########
#########################@#;```` ` #`+#++  #############
##########################@@;;@:@:#   #;#:##@###########
########################@#@+z     `     z +#############
########################@#@@## # z  z # +#`#@###########
#########################@##  #`# z:M@@@@;@W##@#########
########################@#@ `z + ###z ## ###############
########################### :@@@@;:`##W@@#:#@###########
#########################@#z:;;;:;@:@@##  #@############
###########################; # # +z+#  +#` #############
#########################@#::;:#:;;WW;@#:@;#@##@########
############################  `*  + ` +##+ ###@#########
##########################@@z z `+z# ### ` @############
########################@##:#:W@:;@     z+#@@##@########
#########################@#  ##  #+  ` #  ##@#@#########
###########################:### z##@@W@:iWW#############
###########################  ` # ## # ##  #@##@#########
####################+###z+# #++ # ### + #  ###@#########
################### `    ## @iW@#@@ ## # ###@##@########
####################  `  ##@::@@:@;z  + # #@############
################### `   `+ #W;;@@:@+  z # ###@##########
###################    ` #@  +# `   z# # # @############
###################;###*z#### z#   #  +`# +#@@##########
##################@#  ``  + #W;::#Wz ##++ `#@#@#########
################### @#W@@:@   #`# z  `+ z+ #############
####################    #   @W#@@@# ##### ##############
###################@;@,@:,##z;+  #  ` # # ##############
################@##  `   z#W@::#,;; ##  `+ ##@##########
##################### # #+ z+#z ##  * +  ` @##@#########
################@#@++#### z+####  ##z##+ +@@############
################@##:n##+#+ ;:z*z  #    `z@i#@###########
#################@W`.@:@;@;@W@#:;@;;;;:;:@ #############
###################: # + # ##:# ``#;@:@:@###############
#################@#; # # # ;# ::Wi;`z`#`#@:#############
################@## # # # n  z#`.#+::;:::;+@############
##################@`   `   @  #   z+z####+i#@##@########
################@#@ ` `    ` ` `##  + # # #@@@@@########
###################`          #*#+# # #  ` W#@@@########
###################*zz+####+# #`  `###+; # #@W##########
###################        ## #+ # ,;@#@z n#############
###################     `  #+  ####;@;@#``##@###########
################@#@    #+z+  ##    z++z### ##@##########
#################@#*##+ + #  z# # +@;;:;,:@@###@########
################@###++z+`z ++ #  `### ###z+#@@##########
##################@ ` `  + #z# ##+   #z# # @############
#################@#z+++##`++##+    ;;@W@:@;###@#########
###################+z+# +#`    # # ++    #+#@###########
################@##+z#++  #     #+ z#`# z# #@##@########
###################   `##  #### #+  #     z@##@#########
'''

# print('Which Pokémon are you looking for?')
#pkmn: str = input().lower()
pkmn: str = 'ditto'

#if pkmn == 'missingno':
#    print(missingno_ascii)
#    quit()

resp = requests.get('https://pokeapi.co/api/v2/pokemon/{}'.format(pkmn))

if resp.status_code != 200:
    print('\nNo information recorded about such Pokémon\n')
else:
    last_game: str = 'ultra-sun-ultra-moon'     # Update when available
    resp_json = resp.json()

    # HEADER INFO
    print('\n#{} {}\n'.format(resp_json['id'], pkmn.upper()))
    print(' / '.join([tp['type']['name'].capitalize() for tp in resp_json['types']]) + '\n')

    resp_desc = requests.get('https://pokeapi.co/api/v2/pokemon-species/{}'.format(pkmn))
    desc: str = ''

    if resp_desc.status_code != 200:
        desc = 'COULDN\'T GET POKÉMON DESCRIPTION, TRY AGAIN LATER'
    else:
        resp_desc_json = resp_desc.json()['flavor_text_entries']
        eng_descriptions: List[str] = [d['flavor_text'] for d in resp_desc_json if d['language']['name'] == 'en']
        desc_id: int = random.randint(0, len(eng_descriptions) + 1)
        desc = eng_descriptions[desc_id]

    print(desc)
    print()

    # ABILITIES
    print('=> ABILITIES\n')

    for ab in resp_json['abilities']:
        resp_ability = requests.get(ab['ability']['url'])

        if resp_ability.status_code != 200:
            desc = 'COULDN\'T GET ABILITY DESCRIPTION, TRY AGAIN LATER'
        else:
            # Getting the latest description in English
            resp_ability_json = resp_ability.json()
            all_descriptions = resp_ability_json['flavor_text_entries']

            for d in all_descriptions:
                if d['language']['name'] == 'en' and d['version_group']['name'] == last_game:
                    desc = d['flavor_text']
                    break

        print('{}: {}\n'.format(ab['ability']['name'].capitalize(), desc))

    # MOVES
    print('=> MOVES\n')

    for move in resp_json['moves']:
        print(move['move']['name'].capitalize())



    print()
