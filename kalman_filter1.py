#Kalman filter
def predict(mean1, variance1, mean2, variance2):
    mean3 = mean1 + mean2
    var3 = variance1 + variance2
    return [mean3, var3]

def update(mean1, variance1, mean2, variance2):
    mean3 = float(variance2 * mean1 + variance1 * mean2) / (variance1 + variance2)
    var3 = 1/(1/variance1 + 1/variance2)
    return [mean3, var3]

def main():
    measurements = [5.0, 6.0, 7.0, 9.0, 10.0]
    motion = [1.0, 1.0, 2.0, 1.0, 1.0]
    measurement_sig = 4.0
    motion_sig = 2.0
    mu = 2.0
    sig = 1000.0

    for i in range(len(measurements)):
        count = 0
	mu, sig = update(mu, sig, measurements[i], measurement_sig)
        print "update"
        print [mu, sig]
        mu, sig = predict(mu, sig, motion[i], motion_sig)
        print "predict"
        print [mu, sig]
        count += 1

    print(count)

main()

