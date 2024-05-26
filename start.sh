pwd=$(pwd)
model="$pwd/model/feature_extraction"
extractor="chatbot/skills/extractor.py"
feature_extractor="model/feature_extraction/feature_extractor.py"
sed -i "s|ROOT_DIR = .*|ROOT_DIR = \"$pwd\"|" $extractor
sed -i "s|ROOT_DIR = .*|ROOT_DIR = \"$model\"|" $feature_extractor
opsdroid start