package config

import (
	"os"
	"time"

	"github.com/spf13/viper"
)

//Config is
func Config() time.Duration {
	if os.Getenv("ENVIROMENT") == "DEV" {
		viper.SetConfigName("config")
		viper.SetConfigType("toml")
		viper.AddConfigPath("github.com/trafficgen")
		viper.ReadInConfig()
	} else {
		viper.AutomaticEnv()
	}
	timeout := viper.GetDuration("app_timeout")
	return timeout
}
