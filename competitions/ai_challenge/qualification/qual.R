library(MASS)

testing = read.csv('test.csv')
testing$is_weekend_user = as.factor(testing$is_weekend_user)
training = read.csv('train.csv')
training$is_weekend_user = as.factor(training$is_weekend_user)

colSums(is.na(training))

library(rsample)

split_CV = initial_split(training)
train_CV = training(split_CV)
test_CV = testing(split_CV)

library(BART)

x_train = subset(train_CV, select = -c(id, retention))
y_train = train_CV$retention
x_test = subset(test_CV, select = -c(id, retention))
res = lbart(x_train, y_train, x.test = x_test)
test_CV$prob = res$prob.test.mean

library(ROCR)

pred_fit = prediction(test_CV$prob, test_CV$retention)
perf_fit = performance(pred_fit, 'tpr', 'fpr')

perf1 = performance(pred_fit, x.measure = 'cutoff', measure = 'spec')
perf2 = performance(pred_fit, x.measure = 'cutoff', measure = 'sens')
perf3 = performance(pred_fit, x.measure = 'cutoff', measure = 'acc')

plot(perf1, col = 'red', lwd = 2)
plot(add = T, perf2, col = 'green', lwd = 2)
plot(add = T, perf3, col = 'blue', lwd = 2)
abline(v = 0.757, lwd = 2)

x_train = subset(training, select = -c(id, retention))
y_train = training$retention
x_test = subset(testing, select = -c(id))
res = lbart(x_train, y_train, x.test = x_test)

testing$retention = ifelse(res$prob.test.mean >= 0.757, 1, 0)
to_save = testing[c('id', 'retention')]
write.csv(to_save, 'answer.csv', row.names = FALSE)