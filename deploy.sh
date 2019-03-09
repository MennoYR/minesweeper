MODEL_DIR=gs://drs-temp/test
TRAIN_DATA=./train
EVAL_DATA=./eval

gcloud ml-engine jobs submit training $@ \
	--module-name trainer.dqn \
	--package-path trainer/ \
	--job-dir ${MODEL_DIR}
